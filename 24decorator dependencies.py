"""
FastAPI Path Operation Decorator Dependencies Tutorial

This module demonstrates advanced dependency injection patterns using path operation
decorator dependencies in FastAPI. Unlike regular dependencies that inject their
return values into endpoint functions, decorator dependencies execute for validation
and side effects without requiring explicit parameters in the endpoint signature.

Key Concepts:
- Path operation decorator dependencies for security validation
- Dependencies parameter for non-injected dependency execution
- Header-based authentication and authorization patterns
- Multiple security layer implementation through dependency composition

Learning Objectives:
- Master decorator dependency patterns for security enforcement
- Understand when to use dependencies vs regular function parameters
- Implement multi-factor authentication through dependency layering
- Create reusable security validation components

Use Cases:
- API authentication and authorization middleware
- Security header validation across multiple endpoints
- Cross-cutting concerns that don't require data injection
- Validation dependencies that execute before endpoint logic

Architecture Benefits:
- Clean endpoint signatures without security parameter clutter
- Reusable security components across multiple endpoints
- Explicit declaration of endpoint security requirements
- Separation of security logic from business logic

Security Patterns:
- Token-based authentication validation
- API key verification systems
- Multi-layer security enforcement
- Header-based security protocols

Author: FastAPI Tutorial Series
Version: 1.0
Python: 3.11+
FastAPI: 0.104+
"""

from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()

# Create verify_token dependency that checks X-Token header
# Should raise HTTPException(status_code=400) if token != "fake-super-secret-token"
async def verify_token(x_token: Annotated[str, Header()]):
    """
    Security dependency for validating authentication tokens from HTTP headers.
    
    This function serves as a decorator dependency that validates authentication
    tokens without injecting any values into the endpoint function. It demonstrates
    the security validation pattern where dependencies are used purely for their
    side effects (validation/authorization) rather than data injection.
    
    The dependency extracts the X-Token header from incoming HTTP requests and
    validates it against a predefined secret token. If validation fails, it
    raises an HTTP exception that prevents the endpoint from executing.
    
    Args:
        x_token (Annotated[str, Header()]): Authentication token extracted from
            the 'X-Token' HTTP header. FastAPI automatically extracts this header
            and converts it to the parameter name format (X-Token -> x_token).
    
    Returns:
        None: This dependency doesn't return a value as it's used as a decorator
        dependency. Its purpose is validation only, not data injection.
    
    Raises:
        HTTPException: If the token doesn't match the expected value:
            - Status Code: 400 (Bad Request)
            - Detail: "X-Token header invalid"
    
    Example HTTP Requests:
        ```bash
        # Valid request (passes validation)
        curl -H "X-Token: fake-super-secret-token" \
             "http://localhost:8000/items/"
        # Response: [{"item": "Foo"}, {"item": "Bar"}]
        
        # Invalid request (fails validation)
        curl -H "X-Token: wrong-token" \
             "http://localhost:8000/items/"
        # Response: {"detail": "X-Token header invalid"}
        
        # Missing header (fails validation)
        curl "http://localhost:8000/items/"
        # Response: 422 Unprocessable Entity (missing required header)
        ```
    
    Security Considerations:
        - **Hardcoded Token**: For demonstration only - use environment variables in production
        - **Token Exposure**: Consider using Bearer tokens in Authorization header
        - **Token Complexity**: Use cryptographically secure tokens (JWT, UUID, etc.)
        - **Rate Limiting**: Implement rate limiting to prevent brute force attacks
        - **Logging**: Log authentication attempts for security monitoring
    
    Decorator Dependency Pattern:
        ```python
        # Used as decorator dependency (this pattern)
        @app.get("/protected/", dependencies=[Depends(verify_token)])
        async def protected_endpoint():
            # No token parameter needed - validation happens automatically
            return {"message": "Access granted"}
        
        # Regular dependency pattern (alternative)
        @app.get("/protected/")
        async def protected_endpoint(token: str = Depends(verify_token)):
            # Would need to modify function to return token
            return {"message": "Access granted", "token": token}
        ```
    
    Production Enhancements:
        ```python
        import os
        from jose import JWTError, jwt
        
        async def verify_jwt_token(authorization: str = Header(...)):
            try:
                # Extract Bearer token
                if not authorization.startswith("Bearer "):
                    raise HTTPException(401, "Invalid token format")
                
                token = authorization[7:]  # Remove "Bearer " prefix
                
                # Validate JWT
                payload = jwt.decode(
                    token,
                    os.getenv("SECRET_KEY"),
                    algorithms=["HS256"]
                )
                
                # Additional validation
                if payload.get("exp") < time.time():
                    raise HTTPException(401, "Token expired")
                
            except JWTError:
                raise HTTPException(401, "Invalid token")
        ```
    
    Testing Strategies:
        ```python
        from fastapi.testclient import TestClient
        
        def test_valid_token():
            client = TestClient(app)
            response = client.get(
                "/items/",
                headers={"X-Token": "fake-super-secret-token"}
            )
            assert response.status_code == 200
        
        def test_invalid_token():
            client = TestClient(app)
            response = client.get(
                "/items/",
                headers={"X-Token": "wrong-token"}
            )
            assert response.status_code == 400
            assert "X-Token header invalid" in response.json()["detail"]
        
        def test_missing_token():
            client = TestClient(app)
            response = client.get("/items/")
            assert response.status_code == 422  # Missing required header
        ```
    
    Alternative Patterns:
        - **OAuth2 Integration**: Use FastAPI's OAuth2 security schemes
        - **API Key Authentication**: Validate API keys from headers or query parameters
        - **Session-Based Auth**: Validate session cookies for web applications
        - **Multi-Factor Auth**: Combine multiple validation dependencies
    
    Performance Notes:
        - **Minimal Overhead**: Simple string comparison operation
        - **Early Termination**: Fails fast on invalid tokens
        - **No Database Calls**: Static validation for demonstration
        - **Caching**: Consider caching valid tokens in production
    """
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")    

# Create verify_key dependency that checks X-Key header  
# Should raise HTTPException(status_code=400) if key != "fake-super-secret-key"
# Should return the key value

async def verify_key(x_key: Annotated[str, Header()]):
    """
    Authorization dependency for validating API keys with return value capability.
    
    This function demonstrates a hybrid dependency pattern that serves both as a
    decorator dependency for validation and as a regular dependency that can return
    values. It validates API keys from HTTP headers and can optionally inject the
    validated key into endpoint functions for further processing.
    
    The dependency implements a two-factor security approach when combined with
    verify_token, providing both authentication (token) and authorization (key)
    validation layers for enhanced security.
    
    Args:
        x_key (Annotated[str, Header()]): API key extracted from the 'X-Key'
            HTTP header. FastAPI automatically extracts this header and converts
            the header name to parameter format (X-Key -> x_key).
    
    Returns:
        str: The validated API key value. This enables the dependency to be used
        both as a decorator dependency (return value ignored) and as a regular
        dependency (return value injected into endpoint parameters).
    
    Raises:
        HTTPException: If the key doesn't match the expected value:
            - Status Code: 400 (Bad Request)
            - Detail: "X-Key header invalid"
    
    Example HTTP Requests:
        ```bash
        # Valid request with both headers
        curl -H "X-Token: fake-super-secret-token" \
             -H "X-Key: fake-super-secret-key" \
             "http://localhost:8000/items/"
        # Response: [{"item": "Foo"}, {"item": "Bar"}]
        
        # Missing X-Key header
        curl -H "X-Token: fake-super-secret-token" \
             "http://localhost:8000/items/"
        # Response: 422 Unprocessable Entity
        
        # Invalid X-Key header
        curl -H "X-Token: fake-super-secret-token" \
             -H "X-Key: wrong-key" \
             "http://localhost:8000/items/"
        # Response: {"detail": "X-Key header invalid"}
        ```
    
    Dual Usage Patterns:
        ```python
        # Pattern 1: Decorator dependency (current usage)
        @app.get("/items/", dependencies=[Depends(verify_key)])
        async def read_items():
            # Key validation happens, but value not injected
            return [{"item": "data"}]
        
        # Pattern 2: Regular dependency with injection
        @app.get("/items-with-key/")
        async def read_items_with_key(api_key: str = Depends(verify_key)):
            # Key validation happens AND value is injected
            return {"items": [{"item": "data"}], "validated_key": api_key}
        
        # Pattern 3: Combined approach
        @app.get("/items-hybrid/", dependencies=[Depends(verify_token)])
        async def read_items_hybrid(api_key: str = Depends(verify_key)):
            # Token validated as decorator, key validated and injected
            return {"items": [{"item": "data"}], "api_key": api_key}
        ```
    
    Security Architecture:
        - **Authentication Layer**: verify_token ensures user identity
        - **Authorization Layer**: verify_key ensures user permissions
        - **Multi-Factor Security**: Both dependencies required for access
        - **Fail-Fast Validation**: Either failure prevents endpoint execution
    
    API Key Management Best Practices:
        ```python
        import hashlib
        import secrets
        from datetime import datetime, timedelta
        
        # Production-ready key validation
        async def verify_api_key_secure(x_api_key: str = Header(...)):
            # Hash the provided key
            key_hash = hashlib.sha256(x_api_key.encode()).hexdigest()
            
            # Look up in database/cache
            key_info = await get_api_key_info(key_hash)
            
            if not key_info:
                raise HTTPException(401, "Invalid API key")
            
            if key_info["expires_at"] < datetime.utcnow():
                raise HTTPException(401, "API key expired")
            
            if not key_info["is_active"]:
                raise HTTPException(401, "API key deactivated")
            
            # Update last used timestamp
            await update_key_last_used(key_info["id"])
            
            return {
                "key_id": key_info["id"],
                "user_id": key_info["user_id"],
                "permissions": key_info["permissions"]
            }
        ```
    
    Rate Limiting Integration:
        ```python
        from collections import defaultdict
        from time import time
        
        # Simple rate limiter by API key
        key_requests = defaultdict(list)
        
        async def verify_key_with_rate_limit(x_key: str = Header(...)):
            # First validate the key
            if x_key != "fake-super-secret-key":
                raise HTTPException(400, "X-Key header invalid")
            
            # Then check rate limits
            now = time()
            key_requests[x_key] = [
                req_time for req_time in key_requests[x_key]
                if now - req_time < 3600  # 1 hour window
            ]
            
            if len(key_requests[x_key]) >= 1000:  # 1000 requests per hour
                raise HTTPException(429, "Rate limit exceeded")
            
            key_requests[x_key].append(now)
            return x_key
        ```
    
    Testing Comprehensive Scenarios:
        ```python
        def test_valid_key():
            client = TestClient(app)
            response = client.get(
                "/items/",
                headers={
                    "X-Token": "fake-super-secret-token",
                    "X-Key": "fake-super-secret-key"
                }
            )
            assert response.status_code == 200
        
        def test_invalid_key():
            client = TestClient(app)
            response = client.get(
                "/items/",
                headers={
                    "X-Token": "fake-super-secret-token",
                    "X-Key": "wrong-key"
                }
            )
            assert response.status_code == 400
            assert "X-Key header invalid" in response.json()["detail"]
        
        def test_missing_key():
            client = TestClient(app)
            response = client.get(
                "/items/",
                headers={"X-Token": "fake-super-secret-token"}
            )
            assert response.status_code == 422
        
        def test_key_injection():
            # Test when used as regular dependency
            @app.get("/test-key-injection/")
            async def test_endpoint(key: str = Depends(verify_key)):
                return {"injected_key": key}
            
            client = TestClient(app)
            response = client.get(
                "/test-key-injection/",
                headers={"X-Key": "fake-super-secret-key"}
            )
            assert response.status_code == 200
            assert response.json()["injected_key"] == "fake-super-secret-key"
        ```
    
    Enterprise Patterns:
        ```python
        # Scoped API keys with permissions
        async def verify_scoped_key(x_key: str = Header(...)):
            key_data = await validate_api_key(x_key)
            
            return {
                "key": x_key,
                "user_id": key_data["user_id"],
                "scopes": key_data["scopes"],
                "expires_at": key_data["expires_at"]
            }
        
        # Permission-based endpoint protection
        def require_scope(required_scope: str):
            async def scope_dependency(key_data: dict = Depends(verify_scoped_key)):
                if required_scope not in key_data["scopes"]:
                    raise HTTPException(403, f"Scope '{required_scope}' required")
                return key_data
            return scope_dependency
        
        # Usage with scoped permissions
        @app.get("/admin/users/", dependencies=[Depends(require_scope("admin:read"))])
        async def admin_get_users():
            return {"users": get_all_users()}
        ```
    
    Performance Optimization:
        - **Key Caching**: Cache validated keys to reduce database lookups
        - **Async Validation**: Use async database calls for key validation
        - **Connection Pooling**: Optimize database connections for key lookups
        - **Memory Cache**: Use Redis or in-memory cache for frequent validations
    
    Security Monitoring:
        ```python
        import logging
        
        security_logger = logging.getLogger("security")
        
        async def verify_key_with_logging(x_key: str = Header(...)):
            start_time = time.time()
            
            try:
                if x_key != "fake-super-secret-key":
                    security_logger.warning(
                        f"Invalid API key attempt: {x_key[:8]}... from IP: {request.client.host}"
                    )
                    raise HTTPException(400, "X-Key header invalid")
                
                security_logger.info(
                    f"Valid API key used: {x_key[:8]}... validation_time: {time.time() - start_time:.3f}s"
                )
                return x_key
                
            except Exception as e:
                security_logger.error(f"Key validation error: {str(e)}")
                raise
        ```
    
    This dependency demonstrates the flexibility of FastAPI's dependency system,
    serving both security validation and data injection purposes while maintaining
    clean separation of concerns and reusability across endpoints.
    """
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


# TODO: Create GET /items/ endpoint with both verify_token and verify_key in dependencies parameter
# Use: dependencies=[Depends(verify_token), Depends(verify_key)]
# Return: [{"item": "Foo"}, {"item": "Bar"}]
@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():    
    return [{"item": "Foo"}, {"item": "Bar"}]
    