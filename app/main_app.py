"""
FastAPI Bigger Applications - Main Application Module

This module demonstrates the structure and organization of larger FastAPI applications
using modular design patterns. It showcases:

- **Modular Router Organization**: Separating functionality into dedicated router modules
- **Dependency Injection Patterns**: Global and router-specific dependency management
- **Package Structure**: Organizing code into logical packages and subpackages
- **Security Layers**: Multiple authentication and authorization mechanisms
- **Scalable Architecture**: Patterns that support application growth and maintenance

Architecture Overview:
├── app/
│   ├── main_app.py           # Main application entry point (this file)
│   ├── dependencies.py       # Shared dependency injection functions
│   ├── routers/             # Feature-specific route handlers
│   │   ├── items.py         # Item management endpoints
│   │   └── users.py         # User management endpoints
│   └── internal/            # Internal/admin functionality
│       └── admin.py         # Administrative endpoints

Key Patterns Demonstrated:
- **Router Inclusion**: Modular route organization with include_router()
- **Global Dependencies**: Application-wide security and validation
- **Router-Specific Dependencies**: Feature-specific authentication
- **Prefix Organization**: URL namespace management
- **Tag-Based Documentation**: API documentation organization
- **Custom Response Definitions**: Standardized error responses

This architecture supports:
- **Team Development**: Multiple developers working on different modules
- **Code Reusability**: Shared dependencies and common patterns
- **Testing Isolation**: Independent testing of router modules
- **Deployment Flexibility**: Selective feature deployment
- **Maintenance Efficiency**: Clear separation of concerns

Security Architecture:
- **Global Authentication**: Query token validation for all endpoints
- **Header-Based Auth**: X-Token validation for sensitive operations
- **Admin Protection**: Additional security for administrative functions
- **Layered Security**: Multiple authentication mechanisms working together

Use Cases:
- **Enterprise Applications**: Large-scale business applications
- **Microservice Architecture**: Service decomposition patterns
- **API Gateway Patterns**: Centralized routing and authentication
- **Multi-Team Development**: Collaborative development workflows
"""

# Import the necessary modules for FastAPI application structure
from fastapi import FastAPI, Depends

# Import shared dependency injection functions
from .dependencies import get_query_token, get_token_header

# Import feature-specific router modules
from .routers import items, users

# Import internal/administrative router modules
from .internal import admin


def create_application() -> FastAPI:
    """
    Create and configure the main FastAPI application with modular architecture.
    
    This function demonstrates the factory pattern for FastAPI application creation,
    enabling flexible configuration and testing scenarios.
    
    Returns:
        FastAPI: Configured application instance with all routers and dependencies
    
    Configuration Features:
        - Global dependency injection for authentication
        - Modular router inclusion with specific configurations
        - Standardized error responses and documentation
        - Scalable package organization
    
    Security Configuration:
        - Global query token validation (token=jessica)
        - Header-based authentication for sensitive operations
        - Administrative endpoint protection
        - Layered security architecture
    
    Router Organization:
        - Users: Basic user management operations
        - Items: Item CRUD with token authentication
        - Admin: Administrative operations with enhanced security
    
    Production Considerations:
        - Environment-based configuration
        - Database connection management
        - Logging and monitoring integration
        - Rate limiting and security headers
        - CORS configuration for cross-origin requests
    """
    app = FastAPI(
        title="FastAPI Bigger Applications",
        description="Demonstration of modular FastAPI application architecture",
        version="1.0.0",
        dependencies=[Depends(get_query_token)]  # Global authentication requirement
    )
    
    return app


# Create FastAPI application instance with global dependencies
app = create_application()


def configure_routers(app: FastAPI) -> None:
    """
    Configure and include all application routers with their specific settings.
    
    This function demonstrates the centralized router configuration pattern,
    making it easy to manage router inclusion and their specific requirements.
    
    Args:
        app (FastAPI): The FastAPI application instance to configure
    
    Router Configuration:
        - **Users Router**: Basic user operations without additional dependencies
        - **Items Router**: Item management with token header authentication
        - **Admin Router**: Administrative operations with enhanced security
    
    Configuration Patterns:
        - **Prefix Organization**: URL namespace separation (/admin)
        - **Tag-Based Documentation**: Logical grouping in OpenAPI docs
        - **Dependency Injection**: Router-specific authentication requirements
        - **Custom Response Definitions**: Standardized error response schemas
    
    Security Layers:
        1. **Global Dependencies**: Applied to all routes (query token)
        2. **Router Dependencies**: Applied to specific router groups (header token)
        3. **Endpoint Dependencies**: Applied to individual endpoints
    
    URL Structure:
        - GET /users/ → Users router (global auth only)
        - GET /items/ → Items router (global + header auth)
        - POST /admin/ → Admin router (global + header auth + admin prefix)
    
    Response Standards:
        - 404: Standard "Not found" responses
        - 418: Custom "I'm a teapot" responses for admin operations
        - 403: "Operation forbidden" for restricted operations
    """
    # Include users router with basic configuration
    app.include_router(
        users.router,
        # Users router uses only global dependencies
        # No additional authentication required
    )
    
    # Include items router with token header authentication
    app.include_router(
        items.router,
        # Items router requires both global and header token authentication
        # Configured with prefix, tags, and custom error responses
    )
    
    # Include admin router with enhanced security and configuration
    app.include_router(
        admin.router,
        prefix="/admin",                              # URL namespace separation
        tags=["admin"],                               # Documentation grouping
        dependencies=[Depends(get_token_header)],     # Additional security layer
        responses={418: {"description": "I'm a teapot"}}  # Custom response definition
    )


# Configure all application routers
configure_routers(app)


@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint providing basic application information and health check.
    
    This endpoint serves as:
    - **Health Check**: Verify application is running and responding
    - **API Discovery**: Entry point for API exploration
    - **Authentication Test**: Verify global dependencies are working
    - **Documentation Root**: Starting point for API documentation
    
    Returns:
        dict: Welcome message confirming application is operational
    
    Response Format:
        ```json
        {
            "message": "Hello Bigger Applications!"
        }
        ```
    
    Authentication:
        - **Global Token Required**: Must include ?token=jessica query parameter
        - **No Additional Auth**: Only global dependencies apply
    
    Use Cases:
        - **Load Balancer Health Checks**: Simple endpoint for monitoring
        - **API Client Verification**: Confirm API connectivity
        - **Authentication Testing**: Verify token-based access
        - **Development Verification**: Confirm application startup
    
    Example Usage:
        ```bash
        # Successful request with required token
        curl "http://localhost:8000/?token=jessica"
        
        # Response
        {"message": "Hello Bigger Applications!"}
        
        # Failed request without token
        curl "http://localhost:8000/"
        # Returns: 400 "No Jessica token provided"
        ```
    
    Error Responses:
        - **400 Bad Request**: Missing or invalid token parameter
        - **422 Unprocessable Entity**: Invalid request format
    
    Monitoring Integration:
        ```python
        # Add monitoring and logging
        import logging
        
        @app.get("/")
        async def root():
            logging.info("Root endpoint accessed")
            return {"message": "Hello Bigger Applications!"}
        ```
    
    Production Enhancements:
        - **Version Information**: Include API version in response
        - **Environment Details**: Indicate development/staging/production
        - **Service Status**: Include database and external service health
        - **Metrics Collection**: Track endpoint access patterns
    """
    return {"message": "Hello Bigger Applications!"}
