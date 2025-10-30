"""
FastAPI Dependency Injection - Authentication and Security Module

This module implements security and authentication patterns using FastAPI's dependency
injection system. It demonstrates:

- **Token-Based Authentication**: Header and query parameter validation
- **Dependency Injection Patterns**: Reusable security functions
- **Multi-Layer Security**: Different authentication mechanisms for different access levels
- **Error Handling**: Standardized authentication error responses
- **Security Best Practices**: Token validation and access control

Authentication Mechanisms:
1. **Query Token Authentication**: Global application access control
2. **Header Token Authentication**: Enhanced security for sensitive operations

Security Layers:
- **Global Dependencies**: Applied to all application routes
- **Router-Specific Dependencies**: Applied to groups of related endpoints
- **Endpoint-Specific Dependencies**: Applied to individual operations

Token Types:
- **Query Token**: "jessica" - Basic application access
- **Header Token**: "fake-super-secret-token" - Enhanced security access

Error Responses:
- **400 Bad Request**: Invalid or missing authentication tokens
- **401 Unauthorized**: Authentication required but not provided
- **403 Forbidden**: Authentication provided but insufficient permissions

Production Considerations:
- **Environment Variables**: Store tokens in secure environment variables
- **JWT Tokens**: Use JSON Web Tokens for stateless authentication
- **Rate Limiting**: Implement rate limiting to prevent brute force attacks
- **Token Rotation**: Implement token refresh and rotation mechanisms
- **Audit Logging**: Log authentication attempts and failures

Integration Patterns:
- **Database Authentication**: Validate tokens against user database
- **OAuth2 Integration**: Support for third-party authentication providers
- **Role-Based Access Control**: Implement user roles and permissions
- **Session Management**: Handle user sessions and token expiration
"""

from fastapi import Header, HTTPException


async def get_token_header(x_token: str = Header()):
    """
    Validate X-Token header for enhanced security operations.
    
    This dependency function implements header-based authentication for operations
    requiring elevated security. It's typically applied to:
    - Administrative endpoints
    - Sensitive data operations
    - Protected resource modifications
    - Internal API operations
    
    Args:
        x_token (str): Token provided in X-Token header
    
    Raises:
        HTTPException: 400 error if token is invalid or missing
    
    Security Pattern:
        This function implements the "Bearer Token" pattern using custom headers,
        providing an additional layer of authentication beyond global dependencies.
    
    Usage Examples:
        ```python
        # Apply to individual endpoints
        @app.get("/protected")
        async def protected_endpoint(token_valid: None = Depends(get_token_header)):
            return {"message": "Access granted"}
        
        # Apply to router groups
        router = APIRouter(dependencies=[Depends(get_token_header)])
        
        # Apply to specific router inclusion
        app.include_router(
            admin.router,
            dependencies=[Depends(get_token_header)]
        )
        ```
    
    Client Usage:
        ```bash
        # Successful request with valid header
        curl -H "X-Token: fake-super-secret-token" \
             "http://localhost:8000/admin/"
        
        # Failed request with invalid header
        curl -H "X-Token: invalid-token" \
             "http://localhost:8000/admin/"
        # Returns: 400 "X-Token header invalid"
        
        # Failed request without header
        curl "http://localhost:8000/admin/"
        # Returns: 422 "field required" (missing header)
        ```
    
    Production Implementation:
        ```python
        import os
        import jwt
        from datetime import datetime, timedelta
        
        async def get_token_header(x_token: str = Header()):
            expected_token = os.getenv("API_SECRET_TOKEN")
            
            if not expected_token:
                raise HTTPException(500, "Server configuration error")
            
            if x_token != expected_token:
                # Log failed authentication attempt
                logger.warning(f"Invalid token attempt: {x_token[:8]}...")
                raise HTTPException(400, "Invalid authentication token")
            
            # Log successful authentication
            logger.info("Valid token authentication")
        ```
    
    JWT Token Implementation:
        ```python
        import jwt
        from datetime import datetime, timedelta
        
        async def get_token_header(authorization: str = Header()):
            try:
                # Extract token from "Bearer <token>" format
                token = authorization.replace("Bearer ", "")
                
                # Verify JWT token
                payload = jwt.decode(
                    token, 
                    os.getenv("SECRET_KEY"), 
                    algorithms=["HS256"]
                )
                
                # Check expiration
                if datetime.utcnow() > datetime.fromtimestamp(payload["exp"]):
                    raise HTTPException(401, "Token expired")
                
                return payload["user_id"]
                
            except jwt.InvalidTokenError:
                raise HTTPException(401, "Invalid token")
        ```
    
    Security Considerations:
        - **Token Storage**: Never log or expose tokens in plaintext
        - **Rate Limiting**: Implement rate limiting for authentication attempts
        - **Token Rotation**: Use short-lived tokens with refresh mechanisms
        - **Audit Trails**: Log authentication events for security monitoring
        - **Environment Security**: Store tokens in secure environment variables
    
    Error Handling:
        - **400 Bad Request**: Token provided but invalid
        - **422 Unprocessable Entity**: Header missing entirely
        - **500 Internal Server Error**: Server configuration issues
    """
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    """
    Validate query parameter token for global application access control.
    
    This dependency function implements query parameter-based authentication that
    serves as the primary access control mechanism for the entire application.
    It's applied globally to ensure all endpoints require basic authentication.
    
    Args:
        token (str): Token provided as query parameter (?token=value)
    
    Raises:
        HTTPException: 400 error if token is invalid or missing
    
    Security Pattern:
        This function implements global authentication using query parameters,
        providing a simple but effective access control mechanism suitable for:
        - Development environments
        - Internal APIs
        - Simple authentication requirements
        - API key-based access control
    
    Usage Examples:
        ```python
        # Apply globally to entire application
        app = FastAPI(dependencies=[Depends(get_query_token)])
        
        # Apply to specific router groups
        router = APIRouter(dependencies=[Depends(get_query_token)])
        
        # Apply to individual endpoints
        @app.get("/")
        async def root(token_valid: None = Depends(get_query_token)):
            return {"message": "Authenticated access"}
        ```
    
    Client Usage:
        ```bash
        # Successful request with valid token
        curl "http://localhost:8000/?token=jessica"
        
        # Successful request with additional parameters
        curl "http://localhost:8000/items/?token=jessica&limit=10"
        
        # Failed request without token
        curl "http://localhost:8000/"
        # Returns: 422 "field required"
        
        # Failed request with invalid token
        curl "http://localhost:8000/?token=invalid"
        # Returns: 400 "No Jessica token provided"
        ```
    
    Production Implementation:
        ```python
        import os
        import hashlib
        import secrets
        from datetime import datetime
        
        async def get_query_token(token: str):
            # Validate against environment variable
            expected_token = os.getenv("API_ACCESS_TOKEN")
            
            if not expected_token:
                raise HTTPException(500, "Server configuration error")
            
            # Use secure comparison to prevent timing attacks
            if not secrets.compare_digest(token, expected_token):
                # Log failed authentication with timestamp
                logger.warning(f"Invalid token attempt at {datetime.utcnow()}")
                raise HTTPException(400, "Invalid access token")
            
            # Log successful authentication
            logger.info(f"Valid token authentication at {datetime.utcnow()}")
        ```
    
    Database Token Validation:
        ```python
        from sqlalchemy.orm import Session
        
        async def get_query_token(
            token: str,
            db: Session = Depends(get_database)
        ):
            # Look up token in database
            api_key = db.query(APIKey).filter(
                APIKey.token == token,
                APIKey.is_active == True,
                APIKey.expires_at > datetime.utcnow()
            ).first()
            
            if not api_key:
                raise HTTPException(400, "Invalid or expired token")
            
            # Update last used timestamp
            api_key.last_used = datetime.utcnow()
            db.commit()
            
            return api_key.user_id
        ```
    
    Rate Limiting Integration:
        ```python
        from collections import defaultdict
        import time
        
        # Simple rate limiter
        token_requests = defaultdict(list)
        
        async def get_query_token(token: str):
            current_time = time.time()
            
            # Clean old requests (last 5 minutes)
            token_requests[token] = [
                req_time for req_time in token_requests[token]
                if current_time - req_time < 300
            ]
            
            # Check rate limit (100 requests per 5 minutes)
            if len(token_requests[token]) >= 100:
                raise HTTPException(429, "Rate limit exceeded")
            
            # Validate token
            if token != os.getenv("API_ACCESS_TOKEN"):
                raise HTTPException(400, "Invalid access token")
            
            # Record request
            token_requests[token].append(current_time)
        ```
    
    Security Best Practices:
        - **HTTPS Only**: Always use HTTPS in production to protect tokens
        - **Token Rotation**: Implement regular token rotation policies
        - **Monitoring**: Track token usage patterns and anomalies
        - **Expiration**: Use time-limited tokens when possible
        - **Scope Limitation**: Implement token scopes for different access levels
    
    Error Handling:
        - **400 Bad Request**: Token provided but invalid
        - **422 Unprocessable Entity**: Token parameter missing
        - **429 Too Many Requests**: Rate limit exceeded
        - **500 Internal Server Error**: Server configuration issues
    
    Alternative Implementations:
        - **API Keys**: Database-stored API keys with user association
        - **JWT Tokens**: Stateless tokens with embedded claims
        - **OAuth2**: Industry-standard authorization framework
        - **Session Tokens**: Server-side session management
        - **Certificate-Based**: Client certificate authentication
    """
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")
