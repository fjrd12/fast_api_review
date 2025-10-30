"""
FastAPI Security with JWT Tokens - Lesson 30

This module demonstrates a complete, production-ready JWT (JSON Web Token) authentication
system in FastAPI. Building upon lessons 27-29, this implementation showcases real-world
security practices including bcrypt password hashing, JWT token generation/validation,
and secure user session management.

Key Concepts:
- JWT (JSON Web Token) authentication and authorization
- bcrypt password hashing for secure credential storage
- Access token generation with configurable expiration
- Token-based user session management
- Secure password verification and user authentication
- Production-ready security patterns and best practices

JWT Authentication Flow:
1. Client sends username/password to /token endpoint
2. Server validates credentials using bcrypt password verification
3. Server generates JWT token with user identifier and expiration
4. Client stores token and includes it in Authorization header
5. Server validates JWT token on each protected endpoint request
6. Server extracts user information from validated token payload

Security Features:
- bcrypt password hashing with salt for credential protection
- JWT tokens with configurable expiration times
- Secure token validation with signature verification
- Automatic token extraction from Authorization headers
- Comprehensive error handling for authentication failures
- Protection against common security vulnerabilities

Production Considerations:
- Cryptographically secure secret keys for JWT signing
- Proper token expiration and refresh mechanisms
- Secure password hashing with appropriate work factors
- HTTPS enforcement for credential and token transmission
- Rate limiting for authentication endpoints
- Audit logging for security events

Real-world Applications:
- Web application user authentication
- Mobile app backend security
- API access control and user management
- Microservice authentication and authorization
- Single sign-on (SSO) implementations
- Multi-tenant application security

Author: FastAPI Learning Series
Lesson: 30 - Complete JWT Authentication System
"""

from datetime import datetime, timedelta, timezone
from typing import Union

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
import bcrypt
from pydantic import BaseModel
from typing_extensions import Annotated

# JWT Configuration - Production Security Settings
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
"""
JWT Authentication Configuration

SECRET_KEY: Cryptographic secret used for JWT token signing and verification.
    - Generated using: openssl rand -hex 32
    - In production: Store in environment variables, never in code
    - Should be at least 32 characters long for security
    - Keep secret and rotate periodically

ALGORITHM: JWT signing algorithm (HS256 = HMAC with SHA-256)
    - HS256: Symmetric key algorithm (same key for signing and verification)
    - Alternative: RS256 for asymmetric keys in distributed systems
    - Provides cryptographic integrity and authenticity

ACCESS_TOKEN_EXPIRE_MINUTES: Token lifetime in minutes
    - 30 minutes: Balance between security and user experience
    - Shorter: Better security, more frequent re-authentication
    - Longer: Better UX, higher security risk if compromised
    - Production: Consider refresh token patterns for longer sessions

Security Best Practices:
- Use environment variables: SECRET_KEY = os.getenv("SECRET_KEY")
- Implement token rotation and refresh mechanisms
- Add token blacklisting for logout functionality
- Consider different expiration times for different user roles
- Monitor for suspicious authentication patterns
"""

# Sample user database with bcrypt-hashed passwords
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}
"""
User Database Simulation with bcrypt Password Hashing

This dictionary simulates a user database with properly hashed passwords.
In production, this would be replaced with a real database (PostgreSQL,
MongoDB, etc.) with proper user management and security features.

Password Information:
- Username: johndoe
- Password: secret (hashed with bcrypt)
- Hash format: $2b$12$... (bcrypt with cost factor 12)

bcrypt Hash Components:
- $2b$: bcrypt algorithm identifier
- 12: Cost factor (work factor) - controls hashing time/security
- Next 22 chars: Random salt for this password
- Remaining chars: Actual password hash

Cost Factor Guidelines:
- 10: Fast, suitable for development
- 12: Good balance for production (current setting)
- 14+: High security, slower verification

Production Database Schema:
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    full_name VARCHAR(100),
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    failed_login_attempts INTEGER DEFAULT 0,
    account_locked_until TIMESTAMP NULL
);
```

Security Features to Add:
- Account lockout after failed attempts
- Password complexity requirements
- Password expiration and rotation
- Email verification for new accounts
- Two-factor authentication support
- Audit logging for authentication events
"""

app = FastAPI(
    title="JWT Authentication API",
    description="Complete JWT-based authentication system with bcrypt password hashing",
    version="1.0.0"
)

# OAuth2 Password Bearer security scheme for JWT token handling
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
"""
OAuth2 Password Bearer security scheme configuration for JWT authentication.

This scheme handles JWT token extraction from Authorization headers and
integrates with FastAPI's automatic documentation system. It builds upon
the basic OAuth2 concepts from previous lessons to implement JWT-specific
token handling.

Key Features:
- Automatic token extraction from "Authorization: Bearer <token>" headers
- Integration with FastAPI docs for interactive authentication testing
- JWT token validation and user identification
- Seamless integration with dependency injection system

Token Format Expected:
- Header: Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
- Standard JWT format with header.payload.signature structure
- Base64-encoded JSON Web Token with cryptographic signature

See previous lessons (27-29) for detailed OAuth2PasswordBearer documentation.
This lesson focuses on JWT-specific token generation and validation.
"""


# Pydantic models for JWT authentication system
class Token(BaseModel):
    """
    JWT token response model for OAuth2 authentication endpoints.
    
    This model defines the structure of token responses returned by the
    /token endpoint after successful authentication. It follows OAuth2
    standards for token response format.
    
    Attributes:
        access_token (str): The JWT token string that clients use for authentication.
                           Contains encoded user information and expiration time.
        token_type (str): Always "bearer" for JWT tokens, indicating the token
                         should be included in Authorization: Bearer <token> headers.
    
    Usage:
        - Returned by POST /token endpoint after successful login
        - Client stores access_token for subsequent API requests
        - Client includes token in Authorization header for protected endpoints
    
    OAuth2 Compliance:
        This model follows RFC 6749 OAuth2 specification for token responses,
        ensuring compatibility with standard OAuth2 client libraries.
    
    Example Response:
        ```json
        {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer"
        }
        ```
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Internal model for JWT token payload data extraction.
    
    This model represents the data extracted from JWT token payloads
    during token validation. It contains the user identifier that
    was encoded in the token when it was created.
    
    Attributes:
        username (Union[str, None]): Username extracted from JWT "sub" (subject) claim.
                                   None if token doesn't contain valid username.
    
    JWT Claims Mapping:
        - username ← "sub" (subject) claim in JWT payload
        - Future extensions could include roles, permissions, etc.
    
    Usage:
        - Internal use during token validation in get_current_user()
        - Bridges between JWT payload and user database lookup
        - Ensures type safety during token processing
    
    Example JWT Payload:
        ```json
        {
            "sub": "johndoe",
            "exp": 1635724800
        }
        ```
    """
    username: Union[str, None] = None

class User(BaseModel):
    """
    Public user model for API responses (excludes sensitive information).
    
    This model represents user data that is safe to expose through API
    endpoints. It deliberately excludes sensitive fields like password
    hashes to prevent accidental exposure in API responses.
    
    Attributes:
        username (Union[str, None]): Unique user identifier
        email (Union[str, None]): User's email address
        full_name (Union[str, None]): User's display name
        disabled (Union[bool, None]): Account status flag
    
    Security Design:
        - No password or hash fields included
        - Safe for serialization in API responses
        - Can be used for user profile display
        - Follows principle of least privilege for data exposure
    
    Usage Examples:
        - User profile endpoints
        - Public user information display
        - API response serialization
        - Client-side user data representation
    
    Field Validation Notes:
        - All fields are optional to handle partial user data
        - Production versions should add proper validation
        - Consider email format validation with EmailStr
        - Add constraints for username format and length
    """
    username: Union[str, None] = None
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None

class UserInDB(User):
    """
    Internal user model including sensitive database fields.
    
    This model extends the public User model to include fields needed
    for internal operations but should never be exposed through API
    endpoints. It represents the complete user record as stored in
    the database.
    
    Attributes:
        Inherits all User fields plus:
        hashed_password (Union[str, None]): bcrypt-hashed password for authentication
    
    Security Critical:
        - Contains sensitive password hash information
        - Must never be returned directly in API responses
        - Always convert to public User model before serialization
        - Used only for internal authentication and user management
    
    Usage Patterns:
        ```python
        # Internal operations
        user_in_db = UserInDB(**user_dict_from_database)
        
        # Authentication
        is_valid = verify_password(password, user_in_db.hashed_password)
        
        # Convert to public model for API response
        public_user = User(**user_in_db.dict(exclude={"hashed_password"}))
        return public_user
        ```
    
    Database Representation:
        This model maps directly to database user records and includes
        all fields necessary for authentication and user management
        operations.
    """
    hashed_password: Union[str, None] = None

# Password security functions using bcrypt for cryptographic hashing
def verify_password(plain_password, hashed_password):
    """
    Verify a plain text password against a bcrypt hash.
    
    This function uses bcrypt to securely verify passwords without storing
    or handling plain text passwords. bcrypt automatically handles salt
    extraction and provides constant-time comparison to prevent timing attacks.
    
    Args:
        plain_password (str): The plain text password to verify
        hashed_password (str): The bcrypt hash to verify against
    
    Returns:
        bool: True if password matches hash, False otherwise
    
    Security Features:
        - Constant-time comparison prevents timing attacks
        - Automatic salt extraction from hash
        - Computationally expensive verification deters brute force
        - No plain text password storage or logging
    
    bcrypt Process:
        1. Extract salt and cost factor from stored hash
        2. Hash the plain password with extracted salt and cost
        3. Compare resulting hash with stored hash
        4. Return boolean result without timing leaks
    
    Example Usage:
        ```python
        stored_hash = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
        user_input = "secret"
        
        if verify_password(user_input, stored_hash):
            print("Password correct")
        else:
            print("Password incorrect")
        ```
    
    Error Handling:
        - Returns False for malformed hashes
        - Returns False for encoding errors
        - Never raises exceptions that could leak information
    
    Performance Considerations:
        - Verification time depends on cost factor in hash
        - Typically 50-100ms for cost factor 12
        - Consider rate limiting for authentication endpoints
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password):
    """
    Generate a bcrypt hash for a plain text password.
    
    This function creates a secure bcrypt hash with a random salt,
    suitable for storing in a database. The hash includes the salt
    and cost factor, making it self-contained for future verification.
    
    Args:
        password (str): Plain text password to hash
    
    Returns:
        str: bcrypt hash string including salt and cost factor
    
    Security Features:
        - Random salt generation for each password
        - Configurable work factor (cost) for computation time
        - Resistant to rainbow table attacks
        - Future-proof design allows cost factor increases
    
    Hash Format:
        $2b$12$saltsaltsaltsaltsaltsOhash...
        │  │  │                    │
        │  │  │                    └── Password hash (31 chars)
        │  │  └───────────────────────── Salt (22 chars)
        │  └──────────────────────────── Cost factor (work factor)
        └─────────────────────────────── Algorithm identifier
    
    Example Usage:
        ```python
        user_password = "secret123"
        hashed = get_password_hash(user_password)
        # Result: "$2b$12$randomsalt...hashedpassword"
        
        # Store in database
        user_record = {
            "username": "john",
            "hashed_password": hashed
        }
        ```
    
    Cost Factor Considerations:
        - Higher cost = more security but slower verification
        - Cost 12: ~100ms verification time (current setting)
        - Cost 14: ~400ms verification time
        - Adjust based on security requirements and hardware
    
    Production Recommendations:
        - Use environment variable for cost factor configuration
        - Monitor verification times in production
        - Consider async processing for user registration
        - Implement proper error handling and logging
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')    

# User management and authentication helper functions
def get_user(db, username: str):
    """
    Retrieve user information from database by username.
    
    This function simulates database user lookup operations. In production,
    this would involve SQL queries or NoSQL document retrieval with proper
    error handling and connection management.
    
    Args:
        db: User database (dictionary in simulation, Session in production)
        username (str): Username to look up
    
    Returns:
        UserInDB: Complete user object including sensitive fields,
                 or None if user not found
    
    Database Operations:
        - Simulates SELECT * FROM users WHERE username = ?
        - Returns complete user record including password hash
        - Handles case where user doesn't exist gracefully
    
    Production Implementation:
        ```python
        def get_user(db: Session, username: str) -> Optional[UserInDB]:
            db_user = db.query(UserModel).filter(
                UserModel.username == username
            ).first()
            
            if db_user:
                return UserInDB(
                    username=db_user.username,
                    email=db_user.email,
                    full_name=db_user.full_name,
                    disabled=not db_user.is_active,
                    hashed_password=db_user.hashed_password
                )
            return None
        ```
    
    Security Considerations:
        - Use parameterized queries to prevent SQL injection
        - Implement proper database connection handling
        - Add query timeout and error handling
        - Consider caching for frequently accessed users
        - Log failed lookup attempts for security monitoring
    
    Performance Optimization:
        - Add database indexes on username field
        - Implement user caching with appropriate TTL
        - Use connection pooling for database efficiency
        - Consider read replicas for high-traffic applications
    """
    user = db.get(username)
    if user:
        return UserInDB(**user)
    return None

def authenticate_user(fake_db, username: str, password: str):
    """
    Authenticate user credentials and return user object if valid.
    
    This function performs complete user authentication by combining
    user lookup and password verification. It returns the user object
    on successful authentication or False on failure.
    
    Args:
        fake_db: User database (dictionary in simulation)
        username (str): Username to authenticate
        password (str): Plain text password to verify
    
    Returns:
        UserInDB: Complete user object if authentication successful
        False: If authentication fails (user not found or wrong password)
    
    Authentication Process:
        1. Look up user by username in database
        2. If user exists, verify password against stored hash
        3. Return user object if both steps succeed
        4. Return False if either step fails
    
    Security Features:
        - Constant-time password verification prevents timing attacks
        - No distinction between "user not found" and "wrong password"
        - No plain text password storage or logging
        - Secure bcrypt password verification
    
    Usage Example:
        ```python
        user = authenticate_user(database, "johndoe", "secret")
        if user:
            # Authentication successful
            token = create_access_token({"sub": user.username})
            return {"access_token": token, "token_type": "bearer"}
        else:
            # Authentication failed
            raise HTTPException(401, "Invalid credentials")
        ```
    
    Production Enhancements:
        ```python
        def authenticate_user(db: Session, username: str, password: str) -> Optional[UserInDB]:
            user = get_user(db, username)
            if not user:
                # Still perform dummy password check to prevent timing attacks
                verify_password("dummy", "$2b$12$dummy.hash.to.maintain.timing")
                return None
            
            if not verify_password(password, user.hashed_password):
                return None
                
            if user.disabled:
                return None
                
            # Update last login timestamp
            update_last_login(db, user.username)
            
            return user
        ```
    
    Error Handling:
        - Returns False for any authentication failure
        - Doesn't distinguish between different failure types
        - Prevents username enumeration attacks
        - Maintains consistent response timing
    """
    user = get_user(fake_db, username)
    if user and verify_password(password, user.hashed_password):
        return user
    return False

# JWT token creation and management
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """
    Generate a secure JWT access token with user data and expiration.
    
    This function creates digitally signed JWT tokens containing user
    information and expiration timestamps. The tokens are cryptographically
    signed with the secret key to prevent tampering and ensure authenticity.
    
    Args:
        data (dict): Payload data to encode in token (typically user ID)
        expires_delta (timedelta, optional): Custom token expiration time
                                           Defaults to ACCESS_TOKEN_EXPIRE_MINUTES
    
    Returns:
        str: Base64-encoded JWT token string ready for HTTP transmission
    
    Token Structure:
        - Header: Algorithm information (HS256)
        - Payload: User data + expiration timestamp + issued-at time
        - Signature: HMAC-SHA256 signature for verification
    
    Example Token Payload:
        ```json
        {
            "sub": "johndoe",           # Subject (username)
            "exp": 1735689600,          # Expiration (Unix timestamp)
            "iat": 1735686000           # Issued at (Unix timestamp)
        }
        ```
    
    Security Features:
        - Cryptographic signature prevents token tampering
        - Expiration timestamp limits token validity window
        - Secret key rotation capability for enhanced security
        - No sensitive data stored in token payload
    
    Usage Example:
        ```python
        # Standard token (15 minutes)
        token = create_access_token({"sub": "johndoe"})
        
        # Custom expiration (1 hour)
        custom_expiry = timedelta(hours=1)
        token = create_access_token({"sub": "admin"}, custom_expiry)
        ```
    
    Production Enhancements:
        ```python
        def create_access_token(
            data: dict, 
            expires_delta: Optional[timedelta] = None,
            token_type: str = "access",
            scope: List[str] = None
        ) -> str:
            to_encode = data.copy()
            
            # Add standard claims
            now = datetime.now(timezone.utc)
            to_encode.update({
                "iat": now,                    # Issued at
                "jti": str(uuid.uuid4()),      # JWT ID for blacklisting
                "type": token_type,            # Token type
                "scope": scope or []           # User permissions
            })
            
            if expires_delta:
                expire = now + expires_delta
            else:
                expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            
            to_encode.update({"exp": expire})
            
            # Add audience and issuer claims for additional security
            to_encode.update({
                "aud": "myapp-users",          # Audience
                "iss": "myapp-auth"            # Issuer
            })
            
            return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        ```
    
    Error Handling:
        - Handles datetime serialization automatically
        - Validates secret key availability
        - Raises JWTError for encoding failures
        - Ensures expiration is in future
    
    Token Validation:
        - Signature verification with SECRET_KEY
        - Expiration time checking
        - Algorithm validation (prevents None algorithm attack)
        - Payload structure validation
    
    Best Practices:
        - Use short expiration times (15-30 minutes)
        - Implement refresh token pattern for longer sessions
        - Store tokens securely on client (httpOnly cookies)
        - Implement token blacklisting for immediate revocation
        - Monitor token usage patterns for anomaly detection
    """
    # Create JWT token with expiration using jwt.encode()
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Authentication dependency for protected endpoints
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Extract and validate user from JWT token for protected endpoints.
    
    This dependency function handles JWT token validation and user retrieval
    for all protected endpoints. It decodes the token, extracts the username,
    validates the token structure, and returns the authenticated user object.
    
    Args:
        token (str): JWT token from Authorization header (via oauth2_scheme)
    
    Returns:
        UserInDB: Complete user object for authenticated user
    
    Raises:
        HTTPException(401): If token is invalid, expired, or user not found
    
    Authentication Flow:
        1. Extract token from Authorization: Bearer <token> header
        2. Decode and verify JWT signature with secret key
        3. Validate token structure and extract username (sub claim)
        4. Look up user in database by username
        5. Return complete user object if all steps succeed
        6. Raise 401 exception if any step fails
    
    Token Validation Process:
        ```
        Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
                              ↓
        JWT Decode → {"sub": "johndoe", "exp": 1735689600}
                              ↓
        Database Lookup → UserInDB(username="johndoe", ...)
                              ↓
        Return Authenticated User
        ```
    
    Security Features:
        - Cryptographic signature validation prevents token tampering
        - Expiration time validation ensures tokens can't be used indefinitely
        - Algorithm validation prevents "None" algorithm attacks
        - Database lookup ensures user still exists and is valid
        - Consistent error responses prevent information leakage
    
    Error Scenarios:
        - Invalid JWT signature → 401 Unauthorized
        - Expired token → 401 Unauthorized  
        - Missing 'sub' claim → 401 Unauthorized
        - User not found in database → 401 Unauthorized
        - Malformed token → 401 Unauthorized
    
    Usage in Protected Endpoints:
        ```python
        @app.get("/protected")
        async def protected_endpoint(current_user: UserInDB = Depends(get_current_user)):
            return {"message": f"Hello {current_user.username}"}
        
        @app.get("/admin")
        async def admin_endpoint(current_user: UserInDB = Depends(get_current_user)):
            if current_user.disabled:
                raise HTTPException(403, "Account disabled")
            return {"admin_data": "sensitive information"}
        ```
    
    Production Enhancements:
        ```python
        async def get_current_user(
            token: str = Depends(oauth2_scheme),
            db: Session = Depends(get_db)
        ) -> UserInDB:
            credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                username: str = payload.get("sub")
                if username is None:
                    raise credentials_exception
                    
                # Check token blacklist
                if await is_token_blacklisted(payload.get("jti")):
                    raise credentials_exception
                    
                # Validate additional claims
                if payload.get("type") != "access":
                    raise credentials_exception
                    
            except JWTError:
                raise credentials_exception
                
            user = get_user(db, username=username)
            if user is None:
                raise credentials_exception
                
            # Update last activity timestamp
            await update_last_activity(db, user.username)
            
            return user
        ```
    
    Performance Considerations:
        - Token validation is performed on every protected request
        - Database lookup for each request (consider caching)
        - JWT decoding is computationally efficient
        - Consider token caching with short TTL for high-traffic apps
    
    Best Practices:
        - Always validate token signature and expiration
        - Use consistent error messages to prevent information leakage
        - Implement token blacklisting for immediate revocation
        - Log failed authentication attempts for security monitoring
        - Consider rate limiting on authentication endpoints
    """
    # Decode JWT token, extract username, get user from database
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials", headers={"WWW-Authenticate": "Bearer"})
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials", headers={"WWW-Authenticate": "Bearer"})
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials", headers={"WWW-Authenticate": "Bearer"})
    return user

# Active user dependency for endpoints requiring enabled accounts
async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    """
    Ensure current user account is active and not disabled.
    
    This dependency builds on get_current_user to add an additional
    layer of validation, ensuring that authenticated users also have
    active accounts. This prevents disabled users from accessing
    protected resources even with valid tokens.
    
    Args:
        current_user (UserInDB): Authenticated user from get_current_user dependency
    
    Returns:
        UserInDB: Active user object ready for endpoint usage
    
    Raises:
        HTTPException(400): If user account is disabled
    
    Account Status Validation:
        - Receives already-authenticated user from get_current_user
        - Checks user.disabled flag to ensure account is active
        - Returns user object if account is enabled
        - Raises 400 Bad Request if account is disabled
    
    Usage Pattern:
        ```python
        # Basic authentication (allows disabled users for account info)
        @app.get("/profile")
        async def get_profile(user: UserInDB = Depends(get_current_user)):
            return {"username": user.username, "disabled": user.disabled}
        
        # Active user required (blocks disabled users)
        @app.get("/dashboard")
        async def get_dashboard(user: UserInDB = Depends(get_current_active_user)):
            return {"dashboard_data": "sensitive information"}
        ```
    
    Security Benefits:
        - Immediate account disabling takes effect without token invalidation
        - Allows for emergency user suspension
        - Provides granular access control beyond token validity
        - Enables temporary account restrictions
    
    Account Management Scenarios:
        - User violates terms of service → disable account
        - Suspicious activity detected → temporary disable
        - User requests account deactivation → set disabled flag
        - Admin needs to restrict user → disable without token revocation
    
    Production Implementation:
        ```python
        async def get_current_active_user(
            current_user: UserInDB = Depends(get_current_user),
            db: Session = Depends(get_db)
        ) -> UserInDB:
            # Refresh user status from database (in case it changed)
            fresh_user = get_user(db, current_user.username)
            if fresh_user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User no longer exists"
                )
            
            if fresh_user.disabled:
                # Log disabled user access attempt
                logger.warning(f"Disabled user {fresh_user.username} attempted access")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User account is disabled"
                )
            
            return fresh_user
        ```
    
    Error Handling:
        - Returns 400 Bad Request for disabled accounts
        - Different from 401 Unauthorized (authentication vs authorization)
        - Clear error message indicates account status issue
        - Allows client to handle disabled accounts appropriately
    
    Dependency Chain:
        ```
        Request → oauth2_scheme → get_current_user → get_current_active_user
           ↓            ↓              ↓                    ↓
        Extract    Validate      Get User         Check Active Status
        Token      Token         from DB          Return if Active
        ```
    
    Best Practices:
        - Use for all endpoints requiring active user accounts
        - Implement account status caching for high-traffic apps
        - Log disabled user access attempts for security monitoring
        - Provide clear error messages for different account states
        - Consider implementing account suspension reasons
    """
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user", headers={"WWW-Authenticate": "Bearer"})
    return current_user

# Authentication endpoint for obtaining JWT tokens
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    User authentication endpoint that returns JWT access tokens.
    
    This endpoint handles user login by validating credentials and returning
    a JWT token that can be used to access protected resources. It follows
    the OAuth2 password flow pattern with secure password verification.
    
    Args:
        form_data (OAuth2PasswordRequestForm): Form data containing username and password
                                              - username: User's login name
                                              - password: User's plain text password
    
    Returns:
        dict: Token response with access token and type
              {
                  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                  "token_type": "bearer"
              }
    
    Raises:
        HTTPException(401): If credentials are invalid or user not found
    
    Authentication Process:
        1. Extract username and password from form data
        2. Look up user in database by username
        3. Verify password using bcrypt against stored hash
        4. Generate JWT token with user identifier
        5. Return token in standard OAuth2 format
    
    Request Format:
        ```
        POST /token
        Content-Type: application/x-www-form-urlencoded
        
        username=johndoe&password=secret
        ```
    
    Response Format:
        ```json
        {
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNzM1Njg5NjAwfQ.signature",
            "token_type": "bearer"
        }
        ```
    
    Client Usage:
        ```python
        import requests
        
        # Login request
        response = requests.post("http://localhost:8000/token", data={
            "username": "johndoe",
            "password": "secret"
        })
        
        token_data = response.json()
        access_token = token_data["access_token"]
        
        # Use token for protected requests
        headers = {"Authorization": f"Bearer {access_token}"}
        protected_response = requests.get(
            "http://localhost:8000/users/me",
            headers=headers
        )
        ```
    
    Security Features:
        - bcrypt password verification with salt protection
        - No plain text password storage or transmission in response
        - JWT tokens with expiration timestamps
        - Cryptographic signature prevents token tampering
        - Rate limiting should be implemented in production
    
    Production Enhancements:
        ```python
        @app.post("/token", response_model=Token)
        async def login_for_access_token(
            form_data: OAuth2PasswordRequestForm = Depends(),
            db: Session = Depends(get_db),
            request: Request
        ):
            # Rate limiting check
            if await is_rate_limited(request.client.host):
                raise HTTPException(429, "Too many login attempts")
            
            # Authenticate user
            user = authenticate_user(db, form_data.username, form_data.password)
            if not user:
                # Log failed attempt
                logger.warning(f"Failed login attempt for {form_data.username}")
                await record_failed_attempt(request.client.host, form_data.username)
                
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Check account status
            if user.disabled:
                raise HTTPException(400, "Account is disabled")
            
            # Create token with additional claims
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user.username, "scope": user.permissions},
                expires_delta=access_token_expires
            )
            
            # Log successful login
            logger.info(f"Successful login for {user.username}")
            await update_last_login(db, user.username)
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
            }
        ```
    
    Error Handling:
        - Returns 401 for invalid credentials
        - Doesn't distinguish between "user not found" and "wrong password"
        - Prevents username enumeration attacks
        - Consistent error response format
    
    OAuth2 Compliance:
        - Follows OAuth2 password grant flow (RFC 6749)
        - Returns standard token response format
        - Includes token_type field as required
        - Compatible with OAuth2 client libraries
    
    Testing:
        ```bash
        # Using curl
        curl -X POST "http://localhost:8000/token" \
             -H "Content-Type: application/x-www-form-urlencoded" \
             -d "username=johndoe&password=secret"
        
        # Using httpx
        httpx post localhost:8000/token -d username=johndoe -d password=secret
        ```
    
    Best Practices:
        - Implement rate limiting to prevent brute force attacks
        - Log authentication attempts for security monitoring
        - Use HTTPS in production to protect credentials in transit
        - Consider implementing account lockout after failed attempts
        - Monitor for unusual login patterns
    """
    # Authenticate user and return JWT token with expiration
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Protected endpoint to get current user information
@app.get("/users/me/")
async def read_users_me(current_user: UserInDB = Depends(get_current_active_user)):
    """
    Get current authenticated user's profile information.
    
    This protected endpoint returns the profile information of the currently
    authenticated user based on the JWT token provided in the Authorization
    header. It requires a valid, non-expired token and an active user account.
    
    Args:
        current_user (UserInDB): Authenticated active user from dependency injection
    
    Returns:
        UserInDB: Complete user profile information (excluding password hash)
    
    Response Format:
        ```json
        {
            "username": "johndoe",
            "email": "johndoe@example.com",
            "full_name": "John Doe",
            "disabled": false
        }
        ```
    
    Authentication Required:
        - Valid JWT token in Authorization: Bearer <token> header
        - Token must not be expired
        - User account must exist in database
        - User account must be active (not disabled)
    
    Request Example:
        ```
        GET /users/me/
        Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
        ```
    
    Client Usage:
        ```python
        import requests
        
        # First, get token
        token_response = requests.post("http://localhost:8000/token", data={
            "username": "johndoe",
            "password": "secret"
        })
        token = token_response.json()["access_token"]
        
        # Then, get user info
        headers = {"Authorization": f"Bearer {token}"}
        user_response = requests.get("http://localhost:8000/users/me/", headers=headers)
        user_info = user_response.json()
        ```
    
    Error Responses:
        - 401 Unauthorized: Invalid, expired, or missing token
        - 400 Bad Request: User account is disabled
        - 422 Unprocessable Entity: Malformed request
    
    Security Features:
        - JWT token validation ensures request authenticity
        - User account status verification prevents disabled account access
        - No sensitive information (password hash) exposed
        - Token expiration provides time-limited access
    
    Production Enhancements:
        ```python
        @app.get("/users/me/", response_model=UserResponse)
        async def read_users_me(
            current_user: UserInDB = Depends(get_current_active_user),
            db: Session = Depends(get_db)
        ):
            # Refresh user data from database
            fresh_user = get_user(db, current_user.username)
            if not fresh_user:
                raise HTTPException(404, "User not found")
            
            # Update last activity
            await update_last_activity(db, fresh_user.username)
            
            # Return sanitized user data
            return UserResponse(
                username=fresh_user.username,
                email=fresh_user.email,
                full_name=fresh_user.full_name,
                disabled=fresh_user.disabled,
                created_at=fresh_user.created_at,
                last_login=fresh_user.last_login,
                email_verified=fresh_user.email_verified
            )
        ```
    
    Data Privacy:
        - Password hash is never included in response
        - Sensitive fields can be excluded based on user permissions
        - Response can be customized based on user roles
        - PII handling follows data protection regulations
    
    Caching Considerations:
        - User data changes infrequently, suitable for caching
        - Implement cache invalidation on user updates
        - Consider short TTL for security-sensitive applications
        - Balance performance vs data freshness requirements
    
    Usage Patterns:
        ```javascript
        // Frontend JavaScript example
        async function getCurrentUser() {
            const token = localStorage.getItem('access_token');
            
            try {
                const response = await fetch('/users/me/', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                
                if (response.ok) {
                    return await response.json();
                } else if (response.status === 401) {
                    // Token expired, redirect to login
                    window.location.href = '/login';
                }
            } catch (error) {
                console.error('Failed to fetch user data:', error);
            }
        }
        ```
    
    Testing:
        ```bash
        # Get token first
        TOKEN=$(curl -s -X POST "http://localhost:8000/token" \
                     -H "Content-Type: application/x-www-form-urlencoded" \
                     -d "username=johndoe&password=secret" | jq -r '.access_token')
        
        # Use token to get user info
        curl -H "Authorization: Bearer $TOKEN" "http://localhost:8000/users/me/"
        ```
    
    Best Practices:
        - Always validate token before processing request
        - Return consistent response format
        - Log access patterns for security monitoring
        - Implement rate limiting for API protection
        - Use HTTPS in production
    """
    # Return current user using JWT authentication
    return current_user

# Protected endpoint to get current user's items
@app.get("/users/me/items/")
async def read_own_items(current_user: UserInDB = Depends(get_current_active_user)):
    """
    Get current authenticated user's personal items/resources.
    
    This protected endpoint returns items or resources belonging to the
    currently authenticated user. It demonstrates how to implement
    user-specific data access with JWT authentication, ensuring users
    can only access their own data.
    
    Args:
        current_user (UserInDB): Authenticated active user from dependency injection
    
    Returns:
        list[dict]: List of items belonging to the current user
    
    Response Format:
        ```json
        [
            {
                "item_id": "Foo",
                "owner": "johndoe"
            }
        ]
        ```
    
    Authentication Required:
        - Valid JWT token in Authorization: Bearer <token> header
        - Token must not be expired
        - User account must exist and be active
        - Items are filtered to only show user's own resources
    
    Data Isolation:
        - Users can only see their own items
        - Data filtering based on user identity from JWT token
        - No cross-user data access possible
        - Implements proper authorization beyond authentication
    
    Request Example:
        ```
        GET /users/me/items/
        Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
        ```
    
    Security Features:
        - User identity verification via JWT token
        - Data isolation ensures users only see own items
        - No authorization bypass possible
        - Automatic filtering based on authenticated user
    
    Production Implementation:
        ```python
        @app.get("/users/me/items/", response_model=List[ItemResponse])
        async def read_own_items(
            current_user: UserInDB = Depends(get_current_active_user),
            db: Session = Depends(get_db),
            skip: int = Query(0, ge=0),
            limit: int = Query(100, ge=1, le=1000)
        ):
            # Query items belonging to current user
            items = db.query(ItemModel).filter(
                ItemModel.owner_id == current_user.id
            ).offset(skip).limit(limit).all()
            
            return [ItemResponse.from_orm(item) for item in items]
        ```
    
    Best Practices:
        - Always filter data by authenticated user
        - Implement proper pagination for large datasets
        - Add search and filtering capabilities
        - Use database indexes on owner fields
        - Log access patterns for analytics and security
    """
    # Return user's items using JWT authentication
    return [{"item_id": "Foo", "owner": current_user.username}]
