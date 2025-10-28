"""
21Dependenciesstart.py

Dependencies in FastAPI
======================

This module demonstrates the fundamental concepts of dependency injection in FastAPI,
including how to create, use, and share dependencies across multiple endpoints for
code reuse and better application architecture.

Key Concepts Covered:
- Dependency injection with the Depends() function
- Creating reusable dependency functions
- Annotated type hints for dependency parameters
- Sharing common parameters across endpoints
- Code reuse and DRY (Don't Repeat Yourself) principles

Dependencies are a powerful feature in FastAPI that enable code reuse, better
organization, and cleaner separation of concerns in API applications.

Dependencies:
- fastapi: Web framework with dependency injection system
- typing: Type hints for better code clarity and IDE support

Learning Objectives:
- Understand the concept of dependency injection
- Learn to create and use dependency functions
- Practice sharing common parameters across endpoints
- Implement clean code patterns with dependencies
- Reduce code duplication through dependency reuse

Production Considerations:
- Dependencies can handle authentication, database connections, and shared logic
- Proper dependency design improves code maintainability
- Dependencies enable easier testing through dependency injection
- Consider dependency caching for expensive operations
- Use dependencies for cross-cutting concerns

Author: FastAPI Tutorial Series
Date: October 2025
Version: 1.0
"""

from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

# TODO: Create a dependency function called 'common_parameters'
# It should accept: q (str | None = None), skip (int = 0), limit (int = 100)
# Return: {"q": q, "skip": skip, "limit": limit}
    
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    """
    Common parameters dependency for pagination and filtering.
    
    This dependency function demonstrates the fundamental concept of dependency
    injection in FastAPI. It encapsulates common query parameters that are
    frequently used across multiple endpoints for pagination and search functionality.
    
    Args:
        q (str | None): Search query string for filtering results (optional)
        skip (int): Number of items to skip for pagination (default: 0)
        limit (int): Maximum number of items to return (default: 100)
        
    Returns:
        dict: A dictionary containing the processed parameters
        
    Example Usage:
        This dependency can be injected into any endpoint that needs
        pagination and search functionality:
        
        ```python
        @app.get("/items/")
        async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
            # commons = {"q": "search", "skip": 0, "limit": 10}
            pass
        ```
        
    Query Parameters:
        - ?q=search_term: Filter results by search term
        - ?skip=20: Skip first 20 items (pagination)
        - ?limit=50: Return maximum 50 items
        - ?q=laptop&skip=10&limit=25: Combined usage
        
    Benefits of This Dependency:
        - Code reuse across multiple endpoints
        - Consistent parameter validation
        - Centralized parameter processing logic
        - Easy to modify pagination defaults
        - Better maintainability and testing
        
    Dependency Injection:
        FastAPI automatically calls this function when an endpoint
        declares it as a dependency, passing the appropriate query
        parameters from the HTTP request.
        
    Note:
        This is a basic example. Production dependencies might include
        validation, business logic, database connections, or authentication.
    """
    return {"q": q, "skip": skip, "limit": limit}

# TODO: Create GET /items/ endpoint that uses common_parameters as dependency
# Use: commons: Annotated[dict, Depends(common_parameters)]
@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    """
    Retrieve items with common pagination and filtering parameters.
    
    This endpoint demonstrates how to use dependency injection to share
    common parameters across multiple endpoints. The common_parameters
    dependency provides pagination and search functionality.
    
    Args:
        commons (dict): Injected common parameters containing:
            - q: Search query string for filtering
            - skip: Number of items to skip
            - limit: Maximum number of items to return
            
    Returns:
        dict: The common parameters that would be used for data retrieval
        
    Query Parameters:
        - q (str, optional): Search query to filter items
        - skip (int, optional): Number of items to skip (default: 0)
        - limit (int, optional): Maximum items to return (default: 100)
        
    Example Requests:
        GET /items/
        GET /items/?q=laptop
        GET /items/?skip=10&limit=20
        GET /items/?q=electronics&skip=0&limit=50
        
    Example Response:
        {
            "q": "laptop",
            "skip": 10,
            "limit": 20
        }
        
    Dependency Injection Flow:
        1. Client makes request with query parameters
        2. FastAPI extracts query parameters from URL
        3. FastAPI calls common_parameters() with extracted values
        4. common_parameters() returns processed parameter dict
        5. FastAPI injects the result into this endpoint function
        6. Endpoint function receives the processed parameters
        
    Real-World Usage:
        In a production application, this endpoint would use the
        parameters to query a database or external service:
        
        ```python
        # Use commons for database query
        items = db.query(Item).filter(
            Item.name.contains(commons["q"]) if commons["q"] else True
        ).offset(commons["skip"]).limit(commons["limit"]).all()
        
        return {"items": items, "params": commons}
        ```
        
    Benefits:
        - Consistent parameter handling across endpoints
        - Automatic validation of query parameters
        - Reduced code duplication
        - Easy to modify pagination logic centrally
        
    Note:
        This example returns the parameters for demonstration.
        Production endpoints would use these parameters to fetch actual data.
    """
    # TODO: Return the commons dictionary
    return commons


# TODO: Create GET /users/ endpoint that uses the same dependency pattern
@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    """
    Retrieve users with the same common pagination and filtering parameters.
    
    This endpoint demonstrates how the same dependency can be reused across
    different endpoints, providing consistent parameter handling for users
    while maintaining the same pagination and search functionality as items.
    
    Args:
        commons (dict): Injected common parameters containing:
            - q: Search query string for filtering users
            - skip: Number of users to skip for pagination
            - limit: Maximum number of users to return
            
    Returns:
        dict: The common parameters that would be used for user data retrieval
        
    Query Parameters:
        - q (str, optional): Search query to filter users by name, email, etc.
        - skip (int, optional): Number of users to skip (default: 0)  
        - limit (int, optional): Maximum users to return (default: 100)
        
    Example Requests:
        GET /users/
        GET /users/?q=john
        GET /users/?skip=5&limit=10
        GET /users/?q=admin&skip=0&limit=25
        
    Example Response:
        {
            "q": "john", 
            "skip": 5,
            "limit": 10
        }
        
    Dependency Reuse Benefits:
        - Same parameter validation logic as /items/
        - Consistent API behavior across different resources
        - Single point of change for pagination defaults
        - Reduced maintenance overhead
        - Unified parameter processing
        
    Real-World Implementation:
        In practice, this endpoint would use the commons parameters
        to query user data from a database:
        
        ```python
        # Filter users based on search query
        query = db.query(User)
        if commons["q"]:
            query = query.filter(
                or_(
                    User.name.contains(commons["q"]),
                    User.email.contains(commons["q"])
                )
            )
        
        users = query.offset(commons["skip"]).limit(commons["limit"]).all()
        
        return {
            "users": [user.dict() for user in users],
            "pagination": {
                "skip": commons["skip"],
                "limit": commons["limit"],
                "total": query.count()
            }
        }
        ```
        
    Consistency Advantages:
        - Both /items/ and /users/ endpoints behave identically
        - Same query parameter names and defaults
        - Predictable API interface for clients
        - Easier documentation and client SDK generation
        
    Note:
        This demonstrates the power of dependencies for creating
        consistent, reusable functionality across multiple endpoints.
    """
    # TODO: Return the commons dictionary
    return commons