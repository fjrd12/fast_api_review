"""
FastAPI Security - Simple OAuth2 with Password Flow - Lesson 29

This module demonstrates a complete OAuth2 Password Flow implementation in FastAPI,
building upon lessons 27 and 28 to create a full authentication system with login,
token generation, and user management. This represents a significant step toward
production-ready authentication.

Key Concepts:
- OAuth2 Password Request Flow (username/password login)
- Token generation and validation
- User database simulation and management
- Password hashing (simulated for learning)
- Active/inactive user status handling
- Complete authentication endpoints

Authentication Flow:
1. Client sends username/password to /token endpoint
2. Server validates credentials against user database
3. Server returns access token if credentials valid
4. Client includes token in Authorization header for protected endpoints
5. Server validates token and returns user information

Components:
- User database simulation with hashed passwords
- Login endpoint (/token) for credential validation
- User model definitions (public and database versions)
- Current user dependency with active status checking
- Protected user information endpoint (/users/me)

Real-world Applications:
- Web application login systems
- Mobile app authentication backends
- API access control and user management
- Session-based user identification
- Role-based access control foundations

Production Evolution Path:
- Current: Simulated password hashing and token generation
- Next: Real password hashing (bcrypt) and JWT tokens
- Advanced: Refresh tokens, role-based access, OAuth2 scopes
- Enterprise: Multi-factor auth, OAuth2 providers, audit logging

Author: FastAPI Learning Series
Lesson: 29 - Simple OAuth2 with Password Flow
"""

from typing import Union
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing_extensions import Annotated

# Simulated user database for authentication demonstration
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}
"""
Fake user database simulating a real user storage system.

This dictionary represents what would typically be stored in a database
(PostgreSQL, MongoDB, etc.) in a production application. Each user entry
contains essential information for authentication and user management.

User Credentials for Testing:
- johndoe / secret → Active user (login successful)
- alice / secret2 → Disabled user (login fails with "Inactive user")

Database Structure:
- Key: username (unique identifier)
- Value: User data dictionary with:
  - username: Unique user identifier
  - full_name: Display name for user interface
  - email: User's email address
  - hashed_password: Simulated password hash
  - disabled: Account status flag

Password Mapping (for understanding):
- "fakehashedsecret" ← fake_hash_password("secret")
- "fakehashedsecret2" ← fake_hash_password("secret2")

Production Implementation:
```python
# Real database model (SQLAlchemy example)
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
# Database operations
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()
```

Security Considerations:
- Passwords should never be stored in plain text
- Use proper password hashing (bcrypt, Argon2)
- Implement account lockout after failed attempts
- Add password complexity requirements
- Consider email verification for new accounts
- Implement audit logging for authentication events
"""

app = FastAPI(
    title="Simple OAuth2 Password Flow API",
    description="Complete OAuth2 authentication with username/password login",
    version="1.0.0"
)

# Simulated password hashing function for demonstration
def fake_hash_password(password: str):
    """
    Simulated password hashing function for educational purposes.
    
    This function demonstrates the concept of password hashing without
    implementing real cryptographic security. In production, this would
    be replaced with a proper password hashing library.
    
    Args:
        password (str): Plain text password to "hash"
    
    Returns:
        str: Simulated hashed password with predictable format
    
    How it works:
        - Input: "secret" → Output: "fakehashedsecret"
        - Input: "secret2" → Output: "fakehashedsecret2"
        - Format: "fakehashed" + original_password
    
    Production Implementation:
    ```python
    from passlib.context import CryptContext
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)
    
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    ```
    
    Security Best Practices:
    - Use bcrypt, Argon2, or PBKDF2 for real applications
    - Never store passwords in plain text
    - Add salt to prevent rainbow table attacks
    - Use appropriate work factors (rounds/iterations)
    - Consider password complexity requirements
    - Implement secure password reset mechanisms
    
    Example Usage:
        >>> fake_hash_password("secret")
        'fakehashedsecret'
        >>> fake_hash_password("mypassword123")
        'fakehashedmypassword123'
    """
    return "fakehashed" + password

# OAuth2 Password Bearer security scheme for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
"""
OAuth2 Password Bearer security scheme configuration.

This scheme handles token extraction from Authorization headers and integrates
with the FastAPI documentation system. It points to the /token endpoint where
clients can obtain access tokens using username/password credentials.

Configuration:
- tokenUrl="token": Specifies the endpoint for token acquisition
- Scheme expects: Authorization: Bearer <access_token>
- FastAPI docs integration: Shows "Authorize" button and security requirements

See lessons 27-28 for detailed OAuth2PasswordBearer documentation.
"""

# User model definitions for API responses and internal operations
class User(BaseModel):
    """
    Public user model for API responses and external representation.
    
    This model represents user data that can be safely exposed through
    API endpoints. It excludes sensitive information like passwords
    and includes only data appropriate for client consumption.
    
    Attributes:
        username (str): Unique user identifier
        email (Union[str, None]): User's email address (optional)
        full_name (Union[str, None]): User's display name (optional)
        disabled (Union[bool, None]): Account status flag (optional)
    
    Usage:
        - API response serialization
        - Client-side user data representation
        - User profile information
        - Authentication success responses
    
    Security Note:
        This model deliberately excludes sensitive fields like
        hashed_password to prevent accidental exposure in API responses.
    """
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None    

class UserInDB(User):
    """
    Internal user model that includes sensitive database fields.
    
    This model extends the public User model to include fields that
    are needed for internal operations but should not be exposed
    through API endpoints.
    
    Attributes:
        Inherits all User fields plus:
        hashed_password (str): Cryptographically hashed password
    
    Usage:
        - Database operations and queries
        - Password verification during login
        - Internal user management functions
        - Authentication and authorization logic
    
    Security Note:
        This model should never be returned directly in API responses.
        Always convert to public User model before serialization.
    
    Example Usage:
        ```python
        # Internal operations
        user_in_db = UserInDB(**user_dict_from_db)
        
        # Convert to public model for API response
        public_user = User(**user_in_db.dict(exclude={"hashed_password"}))
        return public_user
        ```
    """
    hashed_password: str

# User management helper functions
def get_user(db, username: str):
    """
    Retrieve user information from the database by username.
    
    This function simulates database user lookup operations that would
    typically involve SQL queries or NoSQL document retrieval in
    production applications.
    
    Args:
        db: User database (dictionary in this simulation)
        username (str): Username to search for
    
    Returns:
        UserInDB: Complete user object including sensitive fields,
                 or None if user not found
    
    Usage Examples:
        ```python
        user = get_user(fake_users_db, "johndoe")
        if user:
            print(f"Found user: {user.username}")
        else:
            print("User not found")
        ```
    
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
        - Always validate input parameters
        - Use parameterized queries to prevent SQL injection
        - Consider caching for frequently accessed users
        - Implement audit logging for user access
        - Add rate limiting for user lookup operations
    """
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def fake_decode_token(token):
    """
    Simulated token decoding function for educational purposes.
    
    This function demonstrates token-to-user resolution without implementing
    real token validation. In production, this would involve JWT decoding,
    signature verification, and expiration checking.
    
    Args:
        token (str): Access token (in this demo, just the username)
    
    Returns:
        UserInDB: User object if token is valid (user exists),
                 None if token is invalid (user not found)
    
    Current Implementation:
        - Token is treated as a username
        - No expiration checking
        - No signature validation
        - No security whatsoever (demo only!)
    
    Production JWT Implementation:
        ```python
        import jwt
        from datetime import datetime
        
        def decode_access_token(token: str) -> Optional[UserInDB]:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                username: str = payload.get("sub")
                
                if username is None:
                    return None
                
                # Check expiration
                exp = payload.get("exp")
                if exp and datetime.utcfromtimestamp(exp) < datetime.utcnow():
                    return None
                
                # Get user from database
                return get_user(database, username)
                
            except jwt.PyJWTError:
                return None
        ```
    
    Security Warning:
        This implementation provides NO SECURITY and is for learning only.
        Never use this pattern in production applications.
    """
    # This doesn't provide any security at all - just for demo
    user = get_user(fake_users_db, token)
    return user

# Authentication dependency functions
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Dependency function to extract and validate current user from access token.
    
    This function combines token extraction (via oauth2_scheme) with token
    validation to provide authenticated user information to protected endpoints.
    
    Args:
        token (str): Access token automatically extracted from Authorization header
                    by the oauth2_scheme dependency
    
    Returns:
        UserInDB: Complete user object including all database fields
    
    Raises:
        HTTPException 401: If token is invalid or user not found
    
    Authentication Flow:
        1. oauth2_scheme extracts token from "Authorization: Bearer <token>" header
        2. fake_decode_token attempts to resolve token to user
        3. If user found, return complete user object
        4. If user not found, raise 401 Unauthorized
    
    Usage in Endpoints:
        ```python
        @app.get("/protected/")
        async def protected_endpoint(
            current_user: UserInDB = Depends(get_current_user)
        ):
            return {"message": f"Hello {current_user.username}"}
        ```
    
    Production Enhancements:
        ```python
        async def get_current_user(token: str = Depends(oauth2_scheme)):
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
            except JWTError:
                raise credentials_exception
            
            user = get_user(database, username)
            if user is None:
                raise credentials_exception
            return user
        ```
    
    Error Handling:
        - Invalid tokens return 401 with "Invalid authentication credentials"
        - Missing tokens handled automatically by oauth2_scheme (401)
        - Expired tokens should return 401 (not implemented in demo)
        - Malformed tokens should return 401 (not implemented in demo)
    """
    user = fake_decode_token(token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return user

async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    """
    Dependency function to ensure current user is active (not disabled).
    
    This function builds upon get_current_user to add an additional layer
    of validation, ensuring that authenticated users are also active/enabled.
    This pattern allows for account suspension without token invalidation.
    
    Args:
        current_user (UserInDB): Authenticated user object from get_current_user dependency
    
    Returns:
        UserInDB: Active user object ready for use in business logic
    
    Raises:
        HTTPException 400: If user account is disabled
    
    Dependency Chain:
        HTTP Request → oauth2_scheme → get_current_user → get_current_active_user
        
    Usage Patterns:
        ```python
        # For endpoints requiring active users only
        @app.get("/active-only/")
        async def active_endpoint(
            user: UserInDB = Depends(get_current_active_user)
        ):
            return {"message": f"Active user: {user.username}"}
        
        # For admin endpoints that can see disabled users
        @app.get("/admin/users/")
        async def admin_endpoint(
            user: UserInDB = Depends(get_current_user)  # Allows disabled users
        ):
            # Admin can see disabled users
            return {"user_status": "disabled" if user.disabled else "active"}
        ```
    
    Account Status Handling:
        - Active users (disabled=False): Pass through normally
        - Disabled users (disabled=True): Raise 400 "Inactive user"
        - Null/None disabled field: Treated as active (backward compatibility)
    
    Production Considerations:
        - Consider different error codes for different disable reasons
        - Implement account suspension logging and audit trails
        - Add temporary suspension vs permanent disable distinction
        - Consider grace periods for account reactivation
        - Implement admin override capabilities
    
    Example Test Cases:
        - johndoe (disabled=False) → Success
        - alice (disabled=True) → HTTP 400 "Inactive user"
        - user with disabled=None → Success (treated as active)
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Authentication endpoints
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    OAuth2 compatible token endpoint for user authentication.
    
    This endpoint implements the OAuth2 "password" grant type, allowing clients
    to exchange username/password credentials for access tokens. It follows
    the OAuth2 specification for password-based authentication flows.
    
    Args:
        form_data (OAuth2PasswordRequestForm): Form data containing:
            - username: User's login identifier
            - password: User's plain text password
            - scope: Optional OAuth2 scopes (not used in this demo)
            - client_id: Optional OAuth2 client identifier
            - client_secret: Optional OAuth2 client secret
    
    Returns:
        dict: Token response containing:
            - access_token: Token for accessing protected endpoints
            - token_type: Always "bearer" for this implementation
    
    Raises:
        HTTPException 401: If username not found or password incorrect
    
    Authentication Process:
        1. Extract username and password from form data
        2. Look up user in database by username
        3. Hash provided password and compare with stored hash
        4. If match, generate and return access token
        5. If no match, return 401 Unauthorized
    
    Request Format:
        ```
        POST /token
        Content-Type: application/x-www-form-urlencoded
        
        username=johndoe&password=secret
        ```
    
    Response Format:
        ```json
        {
            "access_token": "johndoe",
            "token_type": "bearer"
        }
        ```
    
    Usage Examples:
        
        curl Command:
        ```bash
        curl -X POST "http://localhost:8000/token" \
             -H "Content-Type: application/x-www-form-urlencoded" \
             -d "username=johndoe&password=secret"
        ```
        
        Python requests:
        ```python
        import requests
        
        response = requests.post(
            "http://localhost:8000/token",
            data={"username": "johndoe", "password": "secret"}
        )
        token_data = response.json()
        access_token = token_data["access_token"]
        ```
    
    Production Implementation:
        ```python
        from datetime import datetime, timedelta
        import jwt
        
        @app.post("/token")
        async def login_for_access_token(
            form_data: OAuth2PasswordRequestForm = Depends()
        ):
            user = authenticate_user(form_data.username, form_data.password)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user.username}, expires_delta=access_token_expires
            )
            
            return {"access_token": access_token, "token_type": "bearer"}
        ```
    
    Security Considerations:
        - Rate limit login attempts to prevent brute force attacks
        - Log authentication attempts for security monitoring
        - Implement account lockout after failed attempts
        - Use HTTPS to protect credentials in transit
        - Consider implementing CAPTCHA for repeated failures
        - Add audit logging for successful authentications
    
    OAuth2 Compliance:
        This endpoint follows OAuth2 Password Grant specification:
        - Accepts application/x-www-form-urlencoded data
        - Returns access_token and token_type fields
        - Uses standard HTTP status codes
        - Compatible with OAuth2 client libraries
    """
    user = get_user(fake_users_db, form_data.username)
    if not user or not fake_hash_password(form_data.password) == user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: UserInDB = Depends(get_current_active_user)):
    """
    Get current authenticated user information.
    
    This endpoint demonstrates the complete OAuth2 authentication flow,
    from token extraction through user validation to data retrieval.
    It requires a valid access token and ensures the user is active.
    
    Args:
        current_user (UserInDB): Authenticated and active user object
                                automatically injected via dependency chain
    
    Returns:
        User: Public user information (excludes sensitive fields like hashed_password)
    
    Authentication Requirements:
        1. Valid Authorization: Bearer <token> header
        2. Token must resolve to existing user
        3. User account must be active (not disabled)
    
    Dependency Chain Flow:
        Request → oauth2_scheme → get_current_user → get_current_active_user → endpoint
        
    Usage Examples:
        
        Successful Request:
        ```
        GET /users/me
        Authorization: Bearer johndoe
        
        Response: 200 OK
        {
            "username": "johndoe",
            "email": "johndoe@example.com",
            "full_name": "John Doe",
            "disabled": false
        }
        ```
        
        Failed Request (no token):
        ```
        GET /users/me
        
        Response: 401 Unauthorized
        {
            "detail": "Not authenticated"
        }
        ```
        
        Failed Request (disabled user):
        ```
        GET /users/me
        Authorization: Bearer alice
        
        Response: 400 Bad Request
        {
            "detail": "Inactive user"
        }
        ```
        
        curl Command:
        ```bash
        # First, get token
        TOKEN=$(curl -s -X POST "http://localhost:8000/token" \
                     -H "Content-Type: application/x-www-form-urlencoded" \
                     -d "username=johndoe&password=secret" | \
                jq -r '.access_token')
        
        # Then, get user info
        curl -H "Authorization: Bearer $TOKEN" \
             http://localhost:8000/users/me
        ```
    
    Data Security:
        - Returns public User model (excludes hashed_password)
        - Automatic conversion from UserInDB to User for safety
        - No sensitive information exposed in response
        - Follows principle of least privilege for data exposure
    
    Production Enhancements:
        ```python
        @app.get("/users/me", response_model=User)
        async def read_users_me(
            current_user: UserInDB = Depends(get_current_active_user),
            include_roles: bool = Query(False, description="Include user roles")
        ):
            user_data = User(**current_user.dict(exclude={"hashed_password"}))
            
            if include_roles and current_user.is_admin:
                # Add role information for admin users
                user_data.roles = get_user_roles(current_user.username)
            
            return user_data
        ```
    
    Common Use Cases:
        - User profile display in web applications
        - Mobile app user synchronization
        - Account verification in client applications
        - User preference and settings endpoints
        - Administrative user information display
    
    Error Scenarios:
        - Missing token → 401 "Not authenticated"
        - Invalid token → 401 "Invalid authentication credentials"  
        - Disabled user → 400 "Inactive user"
        - Expired token → 401 "Token expired" (not implemented in demo)
    
    Testing with FastAPI Docs:
        1. Navigate to http://localhost:8000/docs
        2. Click "Authorize" button
        3. Enter username: johndoe, password: secret
        4. Click "Authorize"
        5. Try the GET /users/me endpoint
        6. Should return user information successfully
    """
    # Convert UserInDB to public User model to exclude sensitive fields
    return User(**current_user.dict(exclude={"hashed_password"}))


# Application startup messages and comprehensive usage guide
print("🔐 FastAPI Simple OAuth2 Password Flow - Ready!")
print("💡 Complete Authentication System Features:")
print("   ✅ Username/password login via /token endpoint")
print("   ✅ Access token generation and validation")
print("   ✅ User database simulation with password hashing")
print("   ✅ Active/inactive user status management")
print("   ✅ Protected user information endpoint")
print("   ✅ Complete OAuth2 Password Grant flow")

print("\n📚 Available Endpoints:")
print("   POST /token - Login with username/password to get access token")
print("   GET /users/me - Get current user info (requires authentication)")

print("\n🔑 Test Credentials:")
print("   👤 johndoe / secret - Active user (login successful)")
print("   👤 alice / secret2 - Disabled user (login fails)")

print("\n🧪 Testing Instructions:")
print("   1. Interactive Testing (FastAPI Docs):")
print("      • Open http://localhost:8000/docs")
print("      • Click 'Authorize' button")
print("      • Enter: username=johndoe, password=secret")
print("      • Test GET /users/me endpoint")

print("\n   2. Command Line Testing:")
print("      • Get token: curl -X POST http://localhost:8000/token \\")
print("                         -H 'Content-Type: application/x-www-form-urlencoded' \\")
print("                         -d 'username=johndoe&password=secret'")
print("      • Use token: curl -H 'Authorization: Bearer johndoe' \\")
print("                         http://localhost:8000/users/me")

print("\n🔄 Authentication Flow:")
print("   1️⃣ Client sends username/password to POST /token")
print("   2️⃣ Server validates credentials and returns access_token")
print("   3️⃣ Client includes token in Authorization: Bearer <token> header")
print("   4️⃣ Server validates token and returns protected data")

print("\n🚀 Next Learning Steps:")
print("   • Real password hashing (bcrypt)")
print("   • JWT token implementation")
print("   • Refresh token patterns")
print("   • Role-based access control")
print("   • OAuth2 scopes and permissions")
