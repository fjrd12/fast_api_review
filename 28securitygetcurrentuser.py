"""
FastAPI Security - Get Current User Pattern - Lesson 28

This module demonstrates the next step in FastAPI security implementation:
extracting user information from authentication tokens. Building on lesson 27's
basic token extraction, this lesson shows how to decode tokens and retrieve
current user data for use in protected endpoints.

Key Concepts:
- Token decoding and user identification
- User model definition with Pydantic
- Current user dependency pattern
- User information endpoints
- Token-to-user mapping strategies
- Dependency chaining for authentication

Authentication Flow Evolution:
- Lesson 27: Basic token extraction from Authorization headers
- Lesson 28: Token decoding and user identification (current)
- Future: Token validation, password hashing, user management

Core Patterns:
1. User Model: Pydantic model representing authenticated users
2. Token Decoder: Function to extract user data from tokens
3. Current User Dependency: Reusable dependency for user identification
4. Protected User Endpoints: Routes returning user-specific information

Real-world Applications:
- User profile endpoints (/users/me)
- User-specific data retrieval
- Authentication middleware patterns
- Token-based user session management
- API user identification across endpoints

Production Considerations:
- JWT token decoding with proper validation
- Database user lookup from token claims
- Token expiration and refresh handling
- User state management and caching
- Error handling for invalid tokens and users

Author: FastAPI Learning Series
Lesson: 28 - Security Get Current User Pattern
"""

from typing import Union
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing_extensions import Annotated

app = FastAPI(
    title="Security Get Current User API",
    description="Demonstration of user identification from authentication tokens",
    version="1.0.0"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
"""
OAuth2 Password Bearer security scheme for token-based authentication.

This security scheme continues from lesson 27, providing the foundation
for token extraction that will be used to identify current users.

See lesson 27 documentation for detailed OAuth2PasswordBearer explanation.
This lesson focuses on what happens after token extraction: user identification.
"""

# User model definition for authenticated users
class User(BaseModel):
    """
    Pydantic model representing an authenticated user in the system.
    
    This model defines the structure of user data that will be extracted
    from authentication tokens and used throughout the application for
    user identification and authorization.
    
    Attributes:
        username (str): Unique username identifier for the user.
                       This is typically the primary identifier extracted from tokens.
        email (Union[str, None]): User's email address. Optional field that may
                                 not always be present in token data.
        full_name (Union[str, None]): User's display name or full name.
                                     Optional field for user interface purposes.
        disabled (Union[bool, None]): Flag indicating if user account is disabled.
                                     Used for account status validation.
    
    Usage Examples:
        # Create user from token data
        user = User(
            username="john_doe",
            email="john@example.com",
            full_name="John Doe",
            disabled=False
        )
        
        # Minimal user (only username required)
        user = User(username="jane_doe")
        
        # User with disabled account
        disabled_user = User(
            username="suspended_user",
            disabled=True
        )
    
    Token Integration:
        This model represents the user data that should be embedded in
        authentication tokens (JWT claims, session data, etc.) and extracted
        during the authentication process.
        
        Common JWT claims mapping:
        - username ← "sub" (subject) claim
        - email ← "email" claim  
        - full_name ← "name" claim
        - disabled ← custom "disabled" claim
    
    Production Considerations:
        - Add user roles/permissions for authorization
        - Include user ID for database relationships
        - Add timestamp fields (created_at, last_login)
        - Consider sensitive data exposure in API responses
        - Implement user profile vs public user models
        - Add validation for email format, username rules
        
    Example Production Model:
        ```python
        class User(BaseModel):
            id: int
            username: str = Field(..., min_length=3, max_length=50)
            email: EmailStr
            full_name: Optional[str] = Field(None, max_length=100)
            is_active: bool = True
            is_superuser: bool = False
            roles: List[str] = []
            created_at: datetime
            last_login: Optional[datetime] = None
        ```
    """
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None

# Token decoding function for user identification
def fake_decode_token(token):
    """
    Simulated token decoding function that extracts user information from a token.
    
    This function demonstrates the pattern for converting authentication tokens
    into User objects. In production, this would involve JWT decoding, database
    lookups, or other token validation mechanisms.
    
    Args:
        token (str): The authentication token extracted from the Authorization header.
                    In this demo, any string token is accepted and processed.
    
    Returns:
        User: A User object populated with information "decoded" from the token.
              In this simulation, returns a fake user with the token incorporated
              into the username to demonstrate the decoding process.
    
    Production Implementation Patterns:
        
        JWT Token Decoding:
        ```python
        import jwt
        from datetime import datetime
        
        def decode_jwt_token(token: str) -> User:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                username = payload.get("sub")
                email = payload.get("email")
                full_name = payload.get("name")
                
                if username is None:
                    raise HTTPException(401, "Invalid token: missing subject")
                    
                # Verify token hasn't expired
                exp = payload.get("exp")
                if exp and datetime.utcfromtimestamp(exp) < datetime.utcnow():
                    raise HTTPException(401, "Token has expired")
                    
                return User(
                    username=username,
                    email=email,
                    full_name=full_name
                )
            except jwt.PyJWTError:
                raise HTTPException(401, "Invalid token format")
        ```
        
        Database User Lookup:
        ```python
        def decode_session_token(token: str) -> User:
            # Look up session in database
            session = db.query(UserSession).filter(
                UserSession.token == token,
                UserSession.expires_at > datetime.utcnow()
            ).first()
            
            if not session:
                raise HTTPException(401, "Invalid or expired session")
                
            user = session.user
            if user.disabled:
                raise HTTPException(401, "Account disabled")
                
            return User(
                username=user.username,
                email=user.email,
                full_name=user.full_name,
                disabled=user.disabled
            )
        ```
        
        API Key Validation:
        ```python
        def decode_api_key(token: str) -> User:
            # Validate API key format and lookup user
            api_key = db.query(ApiKey).filter(
                ApiKey.key == token,
                ApiKey.is_active == True
            ).first()
            
            if not api_key:
                raise HTTPException(401, "Invalid API key")
                
            return User(
                username=api_key.user.username,
                email=api_key.user.email
            )
        ```
    
    Error Handling:
        In production, this function should:
        - Validate token format and signature
        - Check token expiration
        - Handle malformed tokens gracefully
        - Verify user still exists and is active
        - Log authentication attempts for security
        
    Security Considerations:
        - Never log token values in plain text
        - Implement rate limiting for token validation
        - Use constant-time comparison for token validation
        - Consider token revocation mechanisms
        - Implement proper error messages that don't leak information
    """
    # Return a User instance with decoded token data
    return User(
        username=token + "fakedecoded", 
        email="john@example.com", 
        full_name="John Doe"
    )   

# Current user dependency for authentication and user identification
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Dependency function that extracts and returns the current authenticated user.
    
    This function demonstrates the core pattern for user identification in FastAPI:
    combining token extraction (from lesson 27) with user decoding to provide
    a complete User object to protected endpoints.
    
    Dependency Chain:
    1. oauth2_scheme extracts token from Authorization: Bearer <token> header
    2. Token is passed to this function as a dependency
    3. fake_decode_token converts token to User object
    4. User object is provided to dependent endpoints
    
    Args:
        token (str): Authentication token automatically extracted by oauth2_scheme
                    dependency. This comes from the Authorization header.
    
    Returns:
        User: Authenticated user object containing user information decoded
              from the token. This object can be used by endpoints for
              user-specific operations.
    
    Usage in Endpoints:
        ```python
        @app.get("/protected/")
        async def protected_endpoint(
            current_user: Annotated[User, Depends(get_current_user)]
        ):
            return {"message": f"Hello {current_user.username}"}
        ```
    
    Dependency Injection Flow:
        HTTP Request with Authorization: Bearer abc123
            │
            ├─ oauth2_scheme extracts "abc123" token
            │
            ├─ get_current_user receives token "abc123"
            │   ├─ Calls fake_decode_token("abc123")
            │   └─ Returns User(username="abc123fakedecoded", ...)
            │
            └─ Endpoint receives User object for business logic
    
    Production Implementation:
        ```python
        from fastapi import HTTPException, status
        
        async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
            try:
                user = decode_and_validate_token(token)
                
                # Additional user validation
                if user.disabled:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Account disabled",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                
                return user
                
            except InvalidTokenError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        ```
    
    Advanced Patterns:
        
        Optional Authentication:
        ```python
        async def get_current_user_optional(
            token: str = Depends(oauth2_scheme_optional)
        ) -> Optional[User]:
            if not token:
                return None
            return decode_token(token)
        ```
        
        Role-Based Dependencies:
        ```python
        def require_role(required_role: str):
            async def role_dependency(
                current_user: User = Depends(get_current_user)
            ):
                if required_role not in current_user.roles:
                    raise HTTPException(403, "Insufficient permissions")
                return current_user
            return role_dependency
        
        # Usage: admin_user = Depends(require_role("admin"))
        ```
        
        Cached User Lookup:
        ```python
        from functools import lru_cache
        
        @lru_cache(maxsize=100)
        def get_user_cached(username: str) -> User:
            return lookup_user_from_database(username)
        ```
    
    Error Handling Considerations:
        - Invalid token format should return 401
        - Expired tokens should return 401
        - Disabled users should return 401
        - Missing users should return 401
        - Rate limit token validation attempts
        - Log authentication failures for security monitoring
    
    Testing Patterns:
        ```python
        # Override dependency for testing
        def get_test_user():
            return User(username="testuser", email="test@example.com")
        
        app.dependency_overrides[get_current_user] = get_test_user
        ```
    """
    user = fake_decode_token(token)
    return user

# User information endpoint demonstrating current user dependency
@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Endpoint that returns information about the currently authenticated user.
    
    This endpoint demonstrates the complete authentication flow from token
    extraction to user identification, showcasing how the dependency chain
    provides clean access to authenticated user data.
    
    Authentication Requirements:
        - Requires valid Authorization: Bearer <token> header
        - Token must be decodable by fake_decode_token function
        - Returns 401 if no token or invalid token provided
    
    Args:
        current_user (User): The authenticated user object automatically
                           injected by the get_current_user dependency.
                           Contains user information decoded from the token.
    
    Returns:
        User: The complete user object containing username, email, full_name,
              and disabled status. This demonstrates how endpoints can access
              all authenticated user information.
    
    HTTP Examples:
        Successful Request:
        ```
        GET /users/me
        Authorization: Bearer mytoken123
        
        Response: 200 OK
        {
            "username": "mytoken123fakedecoded",
            "email": "john@example.com", 
            "full_name": "John Doe",
            "disabled": null
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
        
        Failed Request (invalid token):
        ```
        GET /users/me
        Authorization: Bearer invalid-token
        
        Response: 401 Unauthorized
        {
            "detail": "Could not validate credentials"
        }
        ```
    
    Common Use Cases:
        - User profile display in web applications
        - Mobile app user info synchronization
        - API client user verification
        - User settings and preferences endpoints
        - Account management interfaces
    
    Production Enhancements:
        ```python
        from fastapi import Query
        
        @app.get("/users/me")
        async def read_users_me(
            current_user: Annotated[User, Depends(get_current_user)],
            include_sensitive: bool = Query(False, description="Include sensitive data")
        ):
            # Base user data
            user_data = {
                "username": current_user.username,
                "email": current_user.email,
                "full_name": current_user.full_name
            }
            
            # Add sensitive data only if requested and authorized
            if include_sensitive and current_user.is_admin:
                user_data.update({
                    "last_login": current_user.last_login,
                    "account_created": current_user.created_at,
                    "roles": current_user.roles
                })
            
            return user_data
        ```
    
    Security Considerations:
        - Don't expose sensitive user data unnecessarily
        - Consider rate limiting for user info endpoints
        - Log access to user information for auditing
        - Validate user is accessing their own information
        - Implement field-level permissions for sensitive data
        
    Testing Examples:
        ```python
        def test_read_users_me_with_valid_token():
            response = client.get(
                "/users/me",
                headers={"Authorization": "Bearer testtoken"}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["username"] == "testtokenfakedecoded"
            assert data["email"] == "john@example.com"
        
        def test_read_users_me_without_token():
            response = client.get("/users/me")
            assert response.status_code == 401
        ```
    
    Related Endpoints:
        - PUT /users/me - Update current user information
        - GET /users/me/preferences - Get user preferences
        - POST /users/me/change-password - Change user password
        - DELETE /users/me - Delete current user account
    """
    return current_user


# Application startup messages and educational guidance
print("👤 FastAPI Security - Get Current User Pattern Ready!")
print("💡 Key Features:")
print("   ✅ User model definition with Pydantic")
print("   ✅ Token decoding for user identification")
print("   ✅ Current user dependency pattern")
print("   ✅ User information endpoint (/users/me)")
print("📚 Authentication Flow:")
print("   1️⃣ Client sends: Authorization: Bearer <token>")
print("   2️⃣ oauth2_scheme extracts token from header") 
print("   3️⃣ get_current_user decodes token to User object")
print("   4️⃣ Endpoint receives authenticated User for business logic")
print("🔧 Testing:")
print("   • Use FastAPI docs (/docs) with any token value")
print("   • Try GET /users/me with Authorization: Bearer testtoken")
print("   • Check response contains decoded user information")
print("🚀 Next Steps: Token validation, password hashing, user management")