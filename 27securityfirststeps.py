"""
FastAPI Security First Steps - Lesson 27

This module introduces the foundational concepts of security in FastAPI using
OAuth2 with Password Bearer tokens. This lesson covers the basic setup for
API authentication and authorization, demonstrating how to implement token-based
security with minimal configuration.

Key Concepts:
- OAuth2 Password Bearer token authentication
- FastAPI security integration with OpenAPI/Swagger UI
- Authorization header handling
- Basic token extraction and validation
- Security scheme configuration
- Protected endpoint patterns

Security Flow Overview:
1. Client obtains token from authentication endpoint
2. Client includes token in Authorization header (Bearer <token>)
3. FastAPI extracts and validates token automatically
4. Protected endpoints receive validated token
5. Business logic processes request with authenticated context

Real-world Applications:
- API authentication for web applications
- Mobile app backend security
- Microservice authentication
- SPA (Single Page Application) backends
- RESTful API security implementation

Learning Progression:
- This lesson: Basic OAuth2 setup and token extraction
- Next lessons: Token validation, user authentication, advanced security patterns
- Advanced topics: JWT tokens, refresh tokens, role-based access control

Author: FastAPI Learning Series
Lesson: 27 - Security First Steps with OAuth2
"""

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from typing_extensions import Annotated

app = FastAPI(
    title="Security First Steps API",
    description="Introduction to FastAPI security with OAuth2 Password Bearer tokens",
    version="1.0.0"
)

# OAuth2 Password Bearer security scheme configuration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
"""
OAuth2PasswordBearer security scheme for token-based authentication.

This creates a security scheme that:
- Expects tokens to be provided in the Authorization header
- Uses the "Bearer" token type format: "Authorization: Bearer <token>"
- Configures the OpenAPI documentation to show authentication UI
- Automatically extracts tokens from requests for dependency injection

Parameters:
    tokenUrl (str): The URL where clients can obtain tokens. This is used
                   for OpenAPI documentation and the "Authorize" button in
                   the FastAPI docs UI. The actual token endpoint implementation
                   would be separate.

Security Flow:
    1. Client makes request with: Authorization: Bearer abc123token
    2. FastAPI extracts "abc123token" from the header
    3. Token is passed to dependent functions for validation
    4. If no token provided, FastAPI returns 401 Unauthorized

OpenAPI Integration:
    - Adds "Authorize" button to FastAPI docs (/docs)
    - Shows security scheme in OpenAPI specification
    - Enables interactive testing with authentication
    - Documents required authentication for endpoints

Examples:
    Valid Authorization headers:
    - "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    - "Authorization: Bearer simple-token-123"
    - "Authorization: Bearer api-key-abc-def-456"

Production Considerations:
    - tokenUrl should point to your actual token endpoint
    - Consider using HTTPS in production for secure token transmission
    - Implement proper token validation (JWT, database lookup, etc.)
    - Add token expiration and refresh mechanisms
    - Consider rate limiting on token endpoints
"""


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Protected endpoint that demonstrates basic OAuth2 token authentication.
    
    This endpoint shows the fundamental pattern for protecting FastAPI endpoints
    using OAuth2 Bearer tokens. The token is automatically extracted from the
    Authorization header and passed to the function for processing.
    
    Authentication Flow:
    1. Client sends request with Authorization header: "Bearer <token>"
    2. oauth2_scheme dependency extracts the token automatically
    3. Token is provided as a string parameter to this function
    4. Function can use token for validation or user identification
    5. If no token provided, FastAPI returns 401 Unauthorized automatically
    
    Args:
        token (str): Bearer token extracted from Authorization header.
                    Injected automatically by FastAPI dependency system.
    
    Returns:
        dict: Simple response containing the received token for demonstration.
              In production, this would return actual protected data.
    
    Raises:
        HTTPException 401: Automatically raised by FastAPI if no Authorization
                          header or malformed Bearer token is provided.
    
    Examples:
        Successful request:
        ```
        GET /items/
        Authorization: Bearer my-secret-token
        
        Response: {"token": "my-secret-token"}
        ```
        
        Failed request (no token):
        ```
        GET /items/
        
        Response: 401 Unauthorized
        {
            "detail": "Not authenticated"
        }
        ```
    
    FastAPI Security Features:
        - Automatic token extraction from Authorization header
        - OpenAPI documentation shows padlock icon for this endpoint
        - Interactive docs (/docs) require authentication to test
        - Consistent error responses for missing authentication
    
    Production Implementation Pattern:
        ```python
        @app.get("/protected-data/")
        async def get_protected_data(
            token: Annotated[str, Depends(oauth2_scheme)]
        ):
            # Validate token (JWT decode, database lookup, etc.)
            user = validate_token(token)
            if not user:
                raise HTTPException(401, "Invalid token")
            
            # Return user-specific data
            return get_user_data(user.id)
        ```
    
    Next Steps:
        - Implement actual token validation logic
        - Add user identification and role checking
        - Create token generation endpoint (/token)
        - Add token expiration and refresh mechanisms
        - Implement JWT tokens for stateless authentication
    """
    return {"token": token}


# Application startup messages and educational information
print("🔐 FastAPI Security First Steps - Ready!")
print("💡 Key Features:")
print("   ✅ OAuth2 Password Bearer token authentication")
print("   ✅ Automatic Authorization header parsing")
print("   ✅ OpenAPI security documentation integration")
print("   ✅ Interactive authentication in FastAPI docs")
print("📚 Endpoints:")
print("   GET /items/ - Protected endpoint requiring Bearer token")
print("🔧 Testing:")
print("   • Use FastAPI docs (/docs) and click 'Authorize' button")
print("   • Enter any token value to test authentication")
print("   • Try requests without Authorization header to see 401 response")
print("🚀 Next Steps: Implement token validation, user management, JWT tokens")

