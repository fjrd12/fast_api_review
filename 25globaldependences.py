"""
FastAPI Global Dependencies Tutorial

This module demonstrates the implementation of global dependencies in FastAPI applications,
showcasing how to apply security validation and cross-cutting concerns across all endpoints
automatically. Global dependencies execute for every request to the application, providing
a powerful mechanism for implementing application-wide security, logging, and validation.

Key Concepts:
- Global dependency injection at the application level
- Automatic execution of dependencies for all endpoints
- Application-wide security and validation patterns
- Cross-cutting concerns implementation without endpoint modification

Learning Objectives:
- Master global dependency configuration for entire applications
- Understand the difference between global, router, and endpoint dependencies
- Implement application-wide security without repetitive code
- Create scalable security architectures for large applications

Use Cases:
- Application-wide authentication and authorization
- Global logging and monitoring across all endpoints
- API-wide rate limiting and throttling
- Universal request validation and preprocessing

Architecture Benefits:
- Centralized security management for the entire application
- Reduced code duplication across multiple endpoints
- Consistent security enforcement without manual configuration
- Easy maintenance and updates to application-wide policies

Security Patterns:
- Multi-layer global authentication (token + API key)
- Application-level request validation
- Universal security header requirements
- Global rate limiting and abuse prevention

Performance Considerations:
- Dependencies execute for every request automatically
- Efficient validation patterns to minimize overhead
- Caching strategies for global dependency results
- Optimal ordering of multiple global dependencies

Author: FastAPI Tutorial Series
Version: 1.0
Python: 3.11+
FastAPI: 0.104+
"""

from fastapi import Depends, FastAPI, Header, HTTPException
from typing_extensions import Annotated


# TODO: Create verify_token dependency that checks X-Token header
# Should raise HTTPException(status_code=400) if token != "fake-super-secret-token"
async def verify_token(x_token: Annotated[str, Header()]):
    """
    Global authentication dependency for validating X-Token headers across all endpoints.
    
    This function serves as a global dependency that automatically validates authentication
    tokens for every request to the FastAPI application. When configured as a global
    dependency, it executes before any endpoint function, ensuring comprehensive security
    coverage without requiring explicit dependency declaration on individual endpoints.
    
    The dependency extracts and validates the X-Token header from all incoming HTTP requests,
    implementing a fail-fast security pattern where invalid authentication immediately
    terminates request processing before reaching business logic.
    
    Args:
        x_token (Annotated[str, Header()]): Authentication token extracted from the
            'X-Token' HTTP header. FastAPI automatically extracts this header and
            converts it to parameter format (X-Token -> x_token) for all requests.
    
    Returns:
        None: As a global dependency focused on validation, this function doesn't
        return values for injection. Its primary purpose is security enforcement
        through side effects (raising exceptions for invalid tokens).
    
    Raises:
        HTTPException: If the token doesn't match the expected value:
            - Status Code: 400 (Bad Request)
            - Detail: "Invalid X-Token header"
            - Terminates request processing immediately
    
    Global Dependency Behavior:
        - **Automatic Execution**: Runs for every request to any endpoint
        - **Pre-Endpoint Validation**: Executes before endpoint functions
        - **Application-Wide Security**: No need to declare on individual endpoints
        - **Consistent Enforcement**: Impossible to bypass or forget
    
    Example HTTP Interactions:
        ```bash
        # Valid request (passes global validation)
        curl -H "X-Token: fake-super-secret-token" \
             -H "X-Key: fake-super-secret-key" \
             "http://localhost:8000/items/"
        # Response: [{"item": "Portal Gun"}, {"item": "Plumbus"}]
        
        # Invalid token (fails global validation)
        curl -H "X-Token: wrong-token" \
             -H "X-Key: fake-super-secret-key" \
             "http://localhost:8000/items/"
        # Response: {"detail": "Invalid X-Token header"}
        
        # Missing token header (fails validation)
        curl -H "X-Key: fake-super-secret-key" \
             "http://localhost:8000/items/"
        # Response: 422 Unprocessable Entity (missing required header)
        ```
    
    Global vs Local Dependencies Comparison:
        ```python
        # Without Global Dependencies (repetitive)
        @app.get("/items/", dependencies=[Depends(verify_token)])
        async def read_items(): ...
        
        @app.get("/users/", dependencies=[Depends(verify_token)])
        async def read_users(): ...
        
        @app.get("/orders/", dependencies=[Depends(verify_token)])
        async def read_orders(): ...
        
        # With Global Dependencies (automatic)
        app = FastAPI(dependencies=[Depends(verify_token)])
        
        @app.get("/items/")  # Automatically protected
        async def read_items(): ...
        
        @app.get("/users/")  # Automatically protected
        async def read_users(): ...
        
        @app.get("/orders/")  # Automatically protected
        async def read_orders(): ...
        ```
    
    Security Architecture Benefits:
        - **Impossible to Forget**: Security is enforced automatically
        - **Centralized Management**: Single point of authentication logic
        - **Consistent Behavior**: Same security across all endpoints
        - **Easy Updates**: Modify security in one place
        - **Audit Compliance**: Guaranteed security coverage
    
    Production Security Enhancements:
        ```python
        import os
        import logging
        from jose import JWTError, jwt
        
        security_logger = logging.getLogger("security")
        
        async def verify_jwt_token_global(authorization: str = Header(...)):
            try:
                # Extract Bearer token
                if not authorization.startswith("Bearer "):
                    security_logger.warning("Invalid token format attempted")
                    raise HTTPException(401, "Invalid token format")
                
                token = authorization[7:]
                
                # Validate JWT with environment variable
                payload = jwt.decode(
                    token,
                    os.getenv("JWT_SECRET_KEY"),
                    algorithms=["HS256"]
                )
                
                # Check token expiration
                if payload.get("exp", 0) < time.time():
                    security_logger.warning(f"Expired token used: {payload.get('sub')}")
                    raise HTTPException(401, "Token expired")
                
                # Log successful authentication
                security_logger.info(f"User authenticated: {payload.get('sub')}")
                
            except JWTError as e:
                security_logger.error(f"JWT validation error: {str(e)}")
                raise HTTPException(401, "Invalid token")
        ```
    
    Rate Limiting Integration:
        ```python
        from collections import defaultdict
        from time import time
        
        # Global rate limiting by token
        token_requests = defaultdict(list)
        
        async def verify_token_with_rate_limit(x_token: str = Header(...)):
            # First validate the token
            if x_token != "fake-super-secret-token":
                raise HTTPException(400, "Invalid X-Token header")
            
            # Then apply rate limiting
            now = time()
            token_requests[x_token] = [
                req_time for req_time in token_requests[x_token]
                if now - req_time < 3600  # 1 hour window
            ]
            
            if len(token_requests[x_token]) >= 1000:  # 1000 requests per hour
                raise HTTPException(429, "Rate limit exceeded")
            
            token_requests[x_token].append(now)
        ```
    
    Testing Global Dependencies:
        ```python
        from fastapi.testclient import TestClient
        
        def test_global_token_validation():
            client = TestClient(app)
            
            # Test valid token on multiple endpoints
            headers = {
                "X-Token": "fake-super-secret-token",
                "X-Key": "fake-super-secret-key"
            }
            
            # All endpoints should be protected
            for endpoint in ["/items/", "/users/"]:
                response = client.get(endpoint, headers=headers)
                assert response.status_code == 200
        
        def test_global_token_rejection():
            client = TestClient(app)
            
            # Test invalid token affects all endpoints
            headers = {
                "X-Token": "wrong-token",
                "X-Key": "fake-super-secret-key"
            }
            
            for endpoint in ["/items/", "/users/"]:
                response = client.get(endpoint, headers=headers)
                assert response.status_code == 400
                assert "Invalid X-Token header" in response.json()["detail"]
        ```
    
    Monitoring and Metrics:
        ```python
        from prometheus_client import Counter, Histogram
        
        auth_attempts = Counter(
            "global_auth_attempts_total",
            "Global authentication attempts",
            ["status", "endpoint"]
        )
        
        async def monitored_verify_token(
            x_token: str = Header(...),
            request: Request = None
        ):
            endpoint = request.url.path if request else "unknown"
            
            try:
                if x_token != "fake-super-secret-token":
                    auth_attempts.labels(status="failed", endpoint=endpoint).inc()
                    raise HTTPException(400, "Invalid X-Token header")
                
                auth_attempts.labels(status="success", endpoint=endpoint).inc()
                
            except HTTPException:
                auth_attempts.labels(status="error", endpoint=endpoint).inc()
                raise
        ```
    
    Error Handling Strategies:
        ```python
        async def robust_verify_token(x_token: str = Header(...)):
            try:
                # Primary validation
                if not x_token or x_token != "fake-super-secret-token":
                    raise HTTPException(400, "Invalid X-Token header")
                
            except Exception as e:
                # Log unexpected errors
                logger.error(f"Unexpected error in token validation: {str(e)}")
                
                # Fail securely - deny access on any error
                raise HTTPException(500, "Authentication service unavailable")
        ```
    
    This global dependency ensures comprehensive security coverage across the entire
    FastAPI application, providing robust authentication without requiring explicit
    configuration on individual endpoints.
    """
    # TODO: Check if x_token equals "fake-super-secret-token", raise HTTPException if not
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    


# TODO: Create verify_key dependency that checks X-Key header
# Should raise HTTPException(status_code=400) if key != "fake-super-secret-key"  
# Should return the key value
async def verify_key(x_key: Annotated[str, Header()]):
    """
    Global authorization dependency for validating X-Key headers with return capability.
    
    This function implements the second layer of global security by validating API keys
    from HTTP headers across all endpoints automatically. As a global dependency, it
    executes after verify_token, creating a multi-layered security architecture where
    both authentication (token) and authorization (key) must be valid for request processing.
    
    The dependency demonstrates the hybrid pattern where global dependencies can both
    validate security requirements and optionally return values, though in global context
    the return values are typically not used for injection since endpoints don't declare
    explicit dependency parameters.
    
    Args:
        x_key (Annotated[str, Header()]): API key extracted from the 'X-Key'
            HTTP header. FastAPI automatically extracts this header from all
            incoming requests and validates it globally before endpoint execution.
    
    Returns:
        str: The validated API key value. While returned for potential future use,
        global dependencies typically focus on validation rather than value injection.
        The return value could be used if this dependency is also used locally.
    
    Raises:
        HTTPException: If the key doesn't match the expected value:
            - Status Code: 400 (Bad Request)
            - Detail: "Invalid X-Key header"
            - Immediately terminates request processing
    
    Global Multi-Layer Security Architecture:
        ```
        HTTP Request
            │
            ├─ Global Dependency 1: verify_token(x_token)
            │   ├─ Validates authentication token
            │   └─ Raises 400 if invalid
            │
            ├─ Global Dependency 2: verify_key(x_key)  ← This function
            │   ├─ Validates authorization key
            │   └─ Raises 400 if invalid
            │
            └─ Endpoint Function
                └─ Business logic (only if both validations pass)
        ```
    
    Example Request Flow:
        ```bash
        # Complete valid request (passes both global dependencies)
        curl -H "X-Token: fake-super-secret-token" \
             -H "X-Key: fake-super-secret-key" \
             "http://localhost:8000/users/"
        # Response: [{"username": "Rick"}, {"username": "Morty"}]
        
        # Fails at first global dependency (token)
        curl -H "X-Token: wrong-token" \
             -H "X-Key: fake-super-secret-key" \
             "http://localhost:8000/users/"
        # Response: {"detail": "Invalid X-Token header"}
        # verify_key never executes
        
        # Passes token but fails at second global dependency (key)
        curl -H "X-Token: fake-super-secret-token" \
             -H "X-Key: wrong-key" \
             "http://localhost:8000/users/"
        # Response: {"detail": "Invalid X-Key header"}
        
        # Missing key header (fails validation)
        curl -H "X-Token: fake-super-secret-token" \
             "http://localhost:8000/users/"
        # Response: 422 Unprocessable Entity
        ```
    
    Global Dependency Execution Order:
        FastAPI executes global dependencies in the order they appear in the list:
        ```python
        # Dependencies execute in this exact order:
        app = FastAPI(dependencies=[
            Depends(verify_token),    # 1. First - authentication
            Depends(verify_key),      # 2. Second - authorization
            Depends(log_request),     # 3. Third - logging (if added)
            Depends(rate_limit)       # 4. Fourth - rate limiting (if added)
        ])
        ```
    
    Multi-Layer Security Benefits:
        - **Defense in Depth**: Multiple security layers prevent bypass
        - **Separation of Concerns**: Authentication vs authorization validation
        - **Fail-Fast Pattern**: First failure stops further processing
        - **Comprehensive Coverage**: Both token and key required globally
        - **Audit Trail**: Multiple validation points for security logging
    
    Production API Key Management:
        ```python
        import hashlib
        import asyncio
        from datetime import datetime
        
        async def verify_api_key_production(x_api_key: str = Header(...)):
            try:
                # Hash the key for secure database lookup
                key_hash = hashlib.sha256(x_api_key.encode()).hexdigest()
                
                # Async database lookup with SQL query
                async with get_db_connection() as conn:
                    query = '''
                        SELECT id, user_id, permissions, expires_at, 
                               is_active, rate_limit_per_hour
                        FROM api_keys 
                        WHERE key_hash = $1 AND is_active = true
                    '''
                    key_info = await conn.fetchrow(query, key_hash)
                
                if not key_info:
                    raise HTTPException(401, "Invalid API key")
                
                # Check expiration
                if key_info["expires_at"] < datetime.utcnow():
                    raise HTTPException(401, "API key expired")
                
                # Store key info in request state for endpoint use
                request.state.api_key_info = {
                    "key_id": key_info["id"],
                    "user_id": key_info["user_id"],
                    "permissions": key_info["permissions"],
                    "rate_limit": key_info["rate_limit_per_hour"]
                }
                
                # Update last used timestamp
                asyncio.create_task(update_key_last_used(key_info["id"]))
                
                return x_api_key
                
            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"API key validation error: {str(e)}")
                raise HTTPException(500, "Authorization service unavailable")
        ```
    
    Scoped Authorization Patterns:
        ```python
        from enum import Enum
        
        class Permission(Enum):
            READ = "read"
            WRITE = "write"
            ADMIN = "admin"
        
        async def verify_key_with_permissions(x_key: str = Header(...)):
            # Basic key validation
            key_data = await validate_api_key(x_key)
            
            if not key_data:
                raise HTTPException(401, "Invalid API key")
            
            # Store permissions for endpoint-level checks
            request.state.user_permissions = key_data["permissions"]
            request.state.user_id = key_data["user_id"]
            
            return key_data
        
        def require_permission(permission: Permission):
            # Create permission-specific global dependency
            async def permission_check(request: Request):
                if not hasattr(request.state, "user_permissions"):
                    raise HTTPException(403, "Permission validation required")
                
                if permission.value not in request.state.user_permissions:
                    raise HTTPException(403, f"Permission '{permission.value}' required")
            
            return permission_check
        
        # Different apps with different permission requirements
        read_app = FastAPI(dependencies=[
            Depends(verify_token),
            Depends(verify_key_with_permissions),
            Depends(require_permission(Permission.READ))
        ])
        
        admin_app = FastAPI(dependencies=[
            Depends(verify_token),
            Depends(verify_key_with_permissions),
            Depends(require_permission(Permission.ADMIN))
        ])
        ```
    
    Global Rate Limiting by API Key:
        ```python
        import redis
        from datetime import timedelta
        
        redis_client = redis.Redis(host='localhost', port=6379, db=0)
        
        async def verify_key_with_rate_limiting(x_key: str = Header(...)):
            # First validate the key
            if x_key != "fake-super-secret-key":
                raise HTTPException(400, "Invalid X-Key header")
            
            # Apply rate limiting per key
            key_prefix = f"rate_limit:{x_key}"
            current_hour = datetime.utcnow().strftime("%Y%m%d%H")
            rate_key = f"{key_prefix}:{current_hour}"
            
            # Increment request count
            current_count = redis_client.incr(rate_key)
            
            # Set expiration on first request of the hour
            if current_count == 1:
                redis_client.expire(rate_key, 3600)  # 1 hour
            
            # Check rate limit (1000 requests per hour per key)
            if current_count > 1000:
                raise HTTPException(
                    429,
                    detail={
                        "error": "Rate limit exceeded",
                        "limit": 1000,
                        "reset_time": f"{current_hour}:59:59"
                    }
                )
            
            return x_key
        ```
    
    Testing Global Key Validation:
        ```python
        def test_global_key_validation_order():
            client = TestClient(app)
            
            # Test that key validation happens after token validation
            response = client.get(
                "/items/",
                headers={
                    "X-Token": "wrong-token",  # This fails first
                    "X-Key": "wrong-key"      # This never gets checked
                }
            )
            # Should fail on token, not key
            assert response.status_code == 400
            assert "Invalid X-Token header" in response.json()["detail"]
        
        def test_key_validation_after_valid_token():
            client = TestClient(app)
            
            # Test key validation with valid token
            response = client.get(
                "/items/",
                headers={
                    "X-Token": "fake-super-secret-token",  # Valid
                    "X-Key": "wrong-key"                   # Invalid
                }
            )
            assert response.status_code == 400
            assert "Invalid X-Key header" in response.json()["detail"]
        
        def test_both_global_validations_pass():
            client = TestClient(app)
            
            # Test successful validation of both global dependencies
            headers = {
                "X-Token": "fake-super-secret-token",
                "X-Key": "fake-super-secret-key"
            }
            
            for endpoint in ["/items/", "/users/"]:
                response = client.get(endpoint, headers=headers)
                assert response.status_code == 200
        ```
    
    Monitoring Multi-Layer Security:
        ```python
        from prometheus_client import Counter, Histogram
        
        security_layer_metrics = Counter(
            "security_layer_validations_total",
            "Security layer validation attempts",
            ["layer", "status", "endpoint"]
        )
        
        async def monitored_verify_key(
            x_key: str = Header(...),
            request: Request = None
        ):
            endpoint = request.url.path if request else "unknown"
            
            try:
                if x_key != "fake-super-secret-key":
                    security_layer_metrics.labels(
                        layer="authorization",
                        status="failed",
                        endpoint=endpoint
                    ).inc()
                    raise HTTPException(400, "Invalid X-Key header")
                
                security_layer_metrics.labels(
                    layer="authorization",
                    status="success",
                    endpoint=endpoint
                ).inc()
                
                return x_key
                
            except HTTPException:
                security_layer_metrics.labels(
                    layer="authorization",
                    status="error",
                    endpoint=endpoint
                ).inc()
                raise
        ```
    
    Global vs Local Dependency Flexibility:
        ```python
        # This dependency can work both globally AND locally
        
        # Global usage (current pattern)
        app = FastAPI(dependencies=[Depends(verify_key)])
        
        # Local usage when additional key processing needed
        @app.get("/special-endpoint/")
        async def special_endpoint(
            api_key: str = Depends(verify_key)  # Also inject the value
        ):
            # Global validation already happened
            # Local injection provides the key value for business logic
            return {
                "message": "Special data",
                "api_key_used": api_key,
                "key_permissions": get_key_permissions(api_key)
            }
        ```
    
    This global dependency creates a comprehensive authorization layer that works
    in conjunction with authentication to ensure complete security coverage across
    all endpoints automatically, while maintaining flexibility for specialized use cases.
    """
    # TODO: Check if x_key equals "fake-super-secret-key", raise HTTPException if not
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="Invalid X-Key header")
    return x_key


# TODO: Create FastAPI app with global dependencies
# Use: app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])
app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])
"""
FastAPI application instance configured with global dependencies for comprehensive security.

This FastAPI application demonstrates the implementation of global dependencies that
automatically execute for every request across all endpoints. The application enforces
a two-layer security model where both authentication (token) and authorization (key)
validation must pass before any endpoint function executes.

Global Dependencies Configuration:
    dependencies=[Depends(verify_token), Depends(verify_key)]

Security Architecture:
    1. verify_token: Validates X-Token header for authentication
    2. verify_key: Validates X-Key header for authorization
    
Execution Flow:
    Request → verify_token() → verify_key() → Endpoint Function → Response
    
If any global dependency fails, the request is immediately terminated with an
appropriate HTTP error response, and subsequent dependencies and endpoint
functions are never executed.

Benefits:
    - Automatic security enforcement across all endpoints
    - No need to declare dependencies on individual endpoints
    - Consistent security behavior throughout the application
    - Impossible to forget or bypass security validation
    - Centralized security management and updates

Usage:
    All endpoints defined after this app creation automatically inherit
    the global security requirements without explicit declaration.
"""


# TODO: Create GET /items/ endpoint (no dependencies needed - they're global)
# Return: [{"item": "Portal Gun"}, {"item": "Plumbus"}]
@app.get("/items/")
async def read_items():
    """
    Retrieve items from the catalog with automatic global security enforcement.
    
    This endpoint demonstrates how global dependencies provide transparent security
    without requiring explicit dependency declarations in the endpoint signature.
    The function focuses purely on business logic while security validation is
    handled automatically by the global dependency system.
    
    Security:
        - Automatically protected by global verify_token dependency
        - Automatically protected by global verify_key dependency
        - No explicit security parameters needed in function signature
        - Security validation occurs before this function executes
    
    Returns:
        list[dict]: List of available items in the catalog:
            - Each item contains an "item" key with the item name
            - Returns Rick and Morty themed items for demonstration
    
    HTTP Status Codes:
        - 200: Successfully retrieved items (security passed)
        - 400: Invalid X-Token or X-Key header (global dependencies failed)
        - 422: Missing required headers (FastAPI validation failed)
    
    Example Requests:
        ```bash
        # Successful request with valid credentials
        curl -H "X-Token: fake-super-secret-token" \
             -H "X-Key: fake-super-secret-key" \
             "http://localhost:8000/items/"
        
        Response:
        [
            {"item": "Portal Gun"},
            {"item": "Plumbus"}
        ]
        
        # Failed request - invalid token (fails global validation)
        curl -H "X-Token: wrong-token" \
             -H "X-Key: fake-super-secret-key" \
             "http://localhost:8000/items/"
        
        Response:
        {"detail": "Invalid X-Token header"}
        
        # Failed request - invalid key (passes token, fails key validation)
        curl -H "X-Token: fake-super-secret-token" \
             -H "X-Key: wrong-key" \
             "http://localhost:8000/items/"
        
        Response:
        {"detail": "Invalid X-Key header"}
        ```
    
    Global Dependency Benefits:
        - **Clean Function Signature**: No security parameters cluttering the interface
        - **Automatic Protection**: Impossible to forget security validation
        - **Consistent Behavior**: Same security across all endpoints
        - **Business Logic Focus**: Function only handles item retrieval logic
        - **Maintenance Simplicity**: Security updates happen in one place
    
    Real-World Extensions:
        ```python
        # Database integration example
        @app.get("/items/")
        async def read_items(
            skip: int = Query(0, ge=0),
            limit: int = Query(100, le=1000)
        ):
            # Security handled by global dependencies
            # Function focuses on data retrieval
            
            async with get_db() as db:
                items = await db.fetch_items(skip=skip, limit=limit)
                return [{"item": item.name, "id": item.id} for item in items]
        
        # Filtered items with search
        @app.get("/items/")
        async def read_items(q: str = Query(None)):
            # Global security automatically applied
            
            all_items = [
                {"item": "Portal Gun", "category": "weapon"},
                {"item": "Plumbus", "category": "household"},
                {"item": "Meeseeks Box", "category": "utility"}
            ]
            
            if q:
                # Filter items by search query
                filtered_items = [
                    item for item in all_items 
                    if q.lower() in item["item"].lower()
                ]
                return filtered_items
            
            return all_items
        ```
    
    Testing Considerations:
        ```python
        # Test business logic separate from security
        def test_items_endpoint_business_logic():
            # Override global dependencies for pure business logic testing
            app.dependency_overrides[verify_token] = lambda: None
            app.dependency_overrides[verify_key] = lambda: "test-key"
            
            client = TestClient(app)
            response = client.get("/items/")
            
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2
            assert data[0]["item"] == "Portal Gun"
            assert data[1]["item"] == "Plumbus"
            
            # Clean up overrides
            app.dependency_overrides = {}
        
        # Test complete security integration
        def test_items_endpoint_with_security():
            client = TestClient(app)
            
            # Test with valid credentials
            response = client.get(
                "/items/",
                headers={
                    "X-Token": "fake-super-secret-token",
                    "X-Key": "fake-super-secret-key"
                }
            )
            assert response.status_code == 200
            
            # Test security rejection
            response = client.get("/items/")  # No headers
            assert response.status_code == 422
        ```
    
    Performance Notes:
        - Global dependencies execute before endpoint function
        - No performance overhead from explicit dependency declarations
        - Efficient validation with fail-fast behavior
        - FastAPI caches dependency results within request scope
    
    This endpoint showcases the power of global dependencies in creating secure
    applications where business logic remains clean and focused while comprehensive
    security is automatically enforced across all endpoints.
    """
    return [{"item": "Portal Gun"}, {"item": "Plumbus"}]



# TODO: Create GET /users/ endpoint (no dependencies needed - they're global)
# Return: [{"username": "Rick"}, {"username": "Morty"}]
@app.get("/users/")
async def read_users():
    """
    Retrieve user list with comprehensive global security protection.
    
    This endpoint demonstrates consistent global dependency behavior across multiple
    endpoints in the application. Like all endpoints in this FastAPI application,
    it automatically inherits the global security dependencies without requiring
    explicit security parameter declarations in the function signature.
    
    The endpoint showcases how global dependencies enable developers to focus on
    business logic (user data retrieval) while comprehensive security validation
    is handled transparently by the dependency injection system.
    
    Security:
        - Automatically validates X-Token header via global verify_token dependency
        - Automatically validates X-Key header via global verify_key dependency
        - Enforces consistent security policy across all application endpoints
        - Prevents execution if either security validation fails
    
    Returns:
        list[dict]: List of users in the system:
            - Each user contains a "username" key with the user's name
            - Returns Rick and Morty themed usernames for demonstration
    
    HTTP Status Codes:
        - 200: Successfully retrieved users (all security validations passed)
        - 400: Invalid X-Token or X-Key header (global dependency validation failed)
        - 422: Missing required security headers (FastAPI validation failed)
    
    Example Requests:
        ```bash
        # Successful request with complete valid credentials
        curl -H "X-Token: fake-super-secret-token" \
             -H "X-Key: fake-super-secret-key" \
             "http://localhost:8000/users/"
        
        Response:
        [
            {"username": "Rick"},
            {"username": "Morty"}
        ]
        
        # Security failure scenarios (identical behavior to /items/ endpoint)
        
        # Scenario 1: Invalid token (first global dependency fails)
        curl -H "X-Token: invalid-token" \
             -H "X-Key: fake-super-secret-key" \
             "http://localhost:8000/users/"
        
        Response:
        {"detail": "Invalid X-Token header"}
        
        # Scenario 2: Valid token but invalid key (second global dependency fails)
        curl -H "X-Token: fake-super-secret-token" \
             -H "X-Key: invalid-key" \
             "http://localhost:8000/users/"
        
        Response:
        {"detail": "Invalid X-Key header"}
        
        # Scenario 3: Missing security headers entirely
        curl "http://localhost:8000/users/"
        
        Response:
        422 Unprocessable Entity
        ```
    
    Global Dependency Consistency:
        This endpoint behaves identically to /items/ regarding security:
        - Same authentication requirements (X-Token validation)
        - Same authorization requirements (X-Key validation)
        - Same error responses for security failures
        - Same execution order (token → key → endpoint)
    
    Business Logic Variations:
        ```python
        # User filtering and pagination example
        @app.get("/users/")
        async def read_users(
            active_only: bool = Query(True),
            role: str = Query(None),
            skip: int = Query(0, ge=0),
            limit: int = Query(100, le=1000)
        ):
            # Global security automatically enforced
            # Function focuses on user business logic
            
            users = [
                {"username": "Rick", "active": True, "role": "scientist"},
                {"username": "Morty", "active": True, "role": "student"},
                {"username": "Jerry", "active": False, "role": "unemployed"},
                {"username": "Beth", "active": True, "role": "surgeon"}
            ]
            
            # Apply filters
            if active_only:
                users = [u for u in users if u["active"]]
            
            if role:
                users = [u for u in users if u["role"] == role]
            
            # Apply pagination
            return users[skip:skip + limit]
        
        # User search with global security
        @app.get("/users/search/")
        async def search_users(q: str = Query(..., min_length=1)):
            # Security handled globally, focus on search logic
            
            all_users = [
                {"username": "Rick", "full_name": "Rick Sanchez"},
                {"username": "Morty", "full_name": "Morty Smith"},
                {"username": "Summer", "full_name": "Summer Smith"}
            ]
            
            # Search in username and full_name
            results = [
                user for user in all_users
                if q.lower() in user["username"].lower() 
                or q.lower() in user["full_name"].lower()
            ]
            
            return results
        ```
    
    Testing Global Consistency:
        ```python
        def test_consistent_global_security():
            client = TestClient(app)
            
            # Test that both endpoints have identical security behavior
            endpoints = ["/items/", "/users/"]
            test_cases = [
                {
                    "headers": {
                        "X-Token": "fake-super-secret-token",
                        "X-Key": "fake-super-secret-key"
                    },
                    "expected_status": 200,
                    "description": "Valid credentials"
                },
                {
                    "headers": {
                        "X-Token": "wrong-token",
                        "X-Key": "fake-super-secret-key"
                    },
                    "expected_status": 400,
                    "description": "Invalid token"
                },
                {
                    "headers": {
                        "X-Token": "fake-super-secret-token",
                        "X-Key": "wrong-key"
                    },
                    "expected_status": 400,
                    "description": "Invalid key"
                },
                {
                    "headers": {},
                    "expected_status": 422,
                    "description": "Missing headers"
                }
            ]
            
            for endpoint in endpoints:
                for case in test_cases:
                    response = client.get(endpoint, headers=case["headers"])
                    assert response.status_code == case["expected_status"], \
                           f"{endpoint} failed for {case['description']}"
        
        def test_users_endpoint_specific_logic():
            # Test business logic with security overrides
            app.dependency_overrides[verify_token] = lambda: None
            app.dependency_overrides[verify_key] = lambda: "test-key"
            
            client = TestClient(app)
            response = client.get("/users/")
            
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2
            assert data[0]["username"] == "Rick"
            assert data[1]["username"] == "Morty"
            
            # Clean up
            app.dependency_overrides = {}
        ```
    
    Real-World Database Integration:
        ```python
        @app.get("/users/")
        async def read_users():
            # Global security ensures only authenticated/authorized requests reach here
            
            async with get_database_connection() as db:
                # Safe to perform database operations - security already validated
                users = await db.fetch(
                    "SELECT username, email, created_at FROM users WHERE active = true"
                )
                
                return [
                    {
                        "username": user["username"],
                        "email": user["email"],
                        "member_since": user["created_at"].isoformat()
                    }
                    for user in users
                ]
        ```
    
    Monitoring and Analytics:
        ```python
        @app.get("/users/")
        async def read_users(request: Request):
            # Global security provides authenticated context
            # Can safely access user info for analytics
            
            # Log user access patterns (security context available)
            logger.info(f"User list accessed from IP: {request.client.host}")
            
            # Return user data
            return [{"username": "Rick"}, {"username": "Morty"}]
        ```
    
    Performance Optimization:
        ```python
        from functools import lru_cache
        
        @lru_cache(maxsize=1, ttl=300)  # Cache for 5 minutes
        def get_cached_users():
            # Expensive user data retrieval
            return [{"username": "Rick"}, {"username": "Morty"}]
        
        @app.get("/users/")
        async def read_users():
            # Global security validated automatically
            # Use caching for performance optimization
            return get_cached_users()
        ```
    
    This endpoint demonstrates how global dependencies create consistent security
    behavior across all application endpoints while allowing each endpoint to focus
    on its specific business logic without security implementation concerns.
    """
    return  [{"username": "Rick"}, {"username": "Morty"}]