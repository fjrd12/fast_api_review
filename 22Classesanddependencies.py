"""
FastAPI Class-Based Dependencies Tutorial

This module demonstrates advanced dependency injection patterns in FastAPI using 
class-based dependencies instead of function-based dependencies. It showcases two
different syntaxes for using class dependencies and provides practical examples
of implementing common query parameters through object-oriented design.

Key Concepts:
- Class-based dependency injection for better organization
- Shortcut vs explicit dependency syntax patterns
- Reusable parameter classes for consistent API behavior
- Object-oriented approach to dependency management

Learning Objectives:
- Understand when to use classes vs functions for dependencies
- Master both dependency syntax variations in FastAPI
- Implement pagination and search through class dependencies
- Apply object-oriented design principles to API development

Author: FastAPI Tutorial Series
Version: 1.0
Python: 3.11+
FastAPI: 0.104+
"""

from fastapi import FastAPI, Depends
from typing import Annotated

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


# Create a CommonQueryParams class with __init__ method
# that takes: q (str | None = None), skip (int = 0), limit (int = 100)
# Store these as self.q, self.skip, self.limit
class CommonQueryParams:
    """
    Class-based dependency for common query parameters used across multiple endpoints.
    
    This class encapsulates common pagination and search parameters that are frequently
    used across different API endpoints. It demonstrates the object-oriented approach
    to dependency injection in FastAPI, providing better organization and reusability
    compared to function-based dependencies for complex parameter sets.
    
    The class automatically handles parameter extraction from query strings and provides
    a clean interface for accessing pagination and search functionality throughout the API.
    
    Attributes:
        q (str | None): Optional search query string for filtering results
        skip (int): Number of items to skip for pagination (default: 0)
        limit (int): Maximum number of items to return per page (default: 100)
    
    Example Usage:
        ```python
        @app.get("/items/")
        async def read_items(commons: Annotated[CommonQueryParams, Depends()]):
            # Access pagination parameters through the class instance
            return {
                "search": commons.q,
                "pagination": {"skip": commons.skip, "limit": commons.limit}
            }
        ```
    
    URL Examples:
        - GET /items/ → CommonQueryParams(q=None, skip=0, limit=100)
        - GET /items/?q=laptop → CommonQueryParams(q="laptop", skip=0, limit=100)
        - GET /items/?skip=10&limit=5 → CommonQueryParams(q=None, skip=10, limit=5)
        - GET /items/?q=phone&skip=20&limit=50 → CommonQueryParams(q="phone", skip=20, limit=50)
    
    Benefits over Function Dependencies:
        - Better organization for complex parameter sets
        - Easier to extend with additional methods
        - More intuitive for developers familiar with OOP
        - Can include validation and business logic methods
        - Cleaner type hints and IDE support
    
    Security Notes:
        - Always validate skip and limit values in production
        - Consider implementing maximum limits to prevent abuse
        - Sanitize search queries to prevent injection attacks
        - Log suspicious parameter combinations for monitoring
    
    Production Considerations:
        - Add parameter validation (skip >= 0, limit <= max_allowed)
        - Implement query string sanitization
        - Consider caching for expensive parameter processing
        - Add metrics tracking for pagination usage patterns
    """
    
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        """
        Initialize common query parameters for pagination and search functionality.
        
        This constructor automatically receives and validates query parameters from
        incoming HTTP requests when used as a FastAPI dependency. FastAPI handles
        the parameter extraction and type conversion automatically.
        
        Args:
            q (str | None, optional): Search query string for filtering results.
                Used to search across relevant fields in the dataset. Defaults to None.
            skip (int, optional): Number of items to skip for pagination. 
                Must be non-negative. Defaults to 0.
            limit (int, optional): Maximum number of items to return per page.
                Should be reasonable to prevent performance issues. Defaults to 100.
        
        Raises:
            ValidationError: If FastAPI's automatic validation fails for parameter types
        
        Example:
            ```python
            # These parameters are automatically extracted from query strings:
            # GET /api/items/?q=laptop&skip=10&limit=20
            params = CommonQueryParams(q="laptop", skip=10, limit=20)
            print(f"Search: {params.q}, Skip: {params.skip}, Limit: {params.limit}")
            ```
        
        Note:
            In production, consider adding additional validation:
            - skip should be >= 0
            - limit should be between 1 and a reasonable maximum (e.g., 1000)
            - q should be sanitized to prevent injection attacks
        """
        # TODO: Store the parameters as instance attributes
        self.q = q
        self.skip = skip
        self.limit = limit


# TODO: Create GET /items/ endpoint using CommonQueryParams as dependency
# Use shortcut syntax: commons: Annotated[CommonQueryParams, Depends()]
# Return response dict with q (if provided) and sliced fake_items_db

@app.get("/items/")
async def read_items(commons: Annotated[CommonQueryParams, Depends()]):
    """
    Retrieve items with pagination and optional search using class-based dependency (shortcut syntax).
    
    This endpoint demonstrates the shortcut syntax for class-based dependencies in FastAPI.
    When using `Depends()` without arguments, FastAPI automatically detects the dependency
    class from the type annotation and instantiates it with the appropriate query parameters.
    
    The endpoint provides pagination functionality and optional search capabilities through
    the CommonQueryParams class dependency, returning a filtered and paginated subset of
    the fake items database.
    
    Args:
        commons (CommonQueryParams): Automatically injected dependency containing:
            - q (str | None): Optional search query for filtering items
            - skip (int): Number of items to skip for pagination
            - limit (int): Maximum number of items to return
    
    Returns:
        dict: Response dictionary containing:
            - q (str, optional): Echo of the search query if provided
            - items (list[dict]): Paginated list of items from the database
    
    Raises:
        ValidationError: If query parameters don't match expected types
    
    HTTP Status Codes:
        - 200: Successfully retrieved items
        - 422: Invalid query parameters (automatic FastAPI validation)
    
    Example Requests:
        ```bash
        # Get all items (first 100)
        curl "http://localhost:8000/items/"
        
        # Search for items
        curl "http://localhost:8000/items/?q=laptop"
        
        # Pagination - skip first 10 items, get next 5
        curl "http://localhost:8000/items/?skip=10&limit=5"
        
        # Combined search and pagination
        curl "http://localhost:8000/items/?q=phone&skip=0&limit=20"
        ```
    
    Example Responses:
        ```json
        // Basic request
        {"items": [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]}
        
        // With search query
        {"q": "laptop", "items": [{"item_name": "Foo"}, {"item_name": "Bar"}]}
        
        // With pagination
        {"items": [{"item_name": "Bar"}, {"item_name": "Baz"}]}
        ```
    
    Dependency Syntax Notes:
        - `Depends()` is the shortcut syntax - FastAPI infers the class from type annotation
        - Equivalent to: `Depends(CommonQueryParams)` but more concise
        - FastAPI automatically instantiates CommonQueryParams with query parameters
        - This syntax only works when the dependency class matches the type annotation
    
    Performance Considerations:
        - Database slicing is performed in memory (not suitable for large datasets)
        - In production, implement database-level pagination with OFFSET/LIMIT
        - Consider implementing caching for frequently accessed pages
        - Add query optimization for search functionality
    
    Security Notes:
        - Validate skip and limit parameters to prevent resource exhaustion
        - Sanitize search queries to prevent injection attacks
        - Implement rate limiting to prevent abuse
        - Log search queries for monitoring and analytics
    
    Production Enhancements:
        - Replace fake_items_db with actual database queries
        - Add proper error handling for database failures
        - Implement search indexing for better performance
        - Add response caching for popular queries
        - Include metadata like total count and page information
    """
    # TODO: Create response dict, add q if provided, slice fake_items_db
    response = {}
    if commons.q:
        response["q"] = commons.q
    response["items"] = fake_items_db[commons.skip : commons.skip + commons.limit]
    return response


# TODO: Create GET /users/ endpoint using explicit dependency syntax
# Use: commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
# Return same structure but with "items" key

@app.get("/users/")
async def read_users(commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]):
    """
    Retrieve users with pagination and optional search using class-based dependency (explicit syntax).
    
    This endpoint demonstrates the explicit syntax for class-based dependencies in FastAPI.
    By using `Depends(CommonQueryParams)`, we explicitly specify which class should be used
    as the dependency, providing more clarity and control over the dependency injection process.
    
    Functionally identical to the /items/ endpoint but showcases the alternative dependency
    syntax for educational purposes. Both syntaxes produce the same result but offer different
    levels of explicitness and clarity in the code.
    
    Args:
        commons (CommonQueryParams): Explicitly injected dependency containing:
            - q (str | None): Optional search query for filtering users
            - skip (int): Number of users to skip for pagination
            - limit (int): Maximum number of users to return
    
    Returns:
        dict: Response dictionary containing:
            - q (str, optional): Echo of the search query if provided
            - items (list[dict]): Paginated list of users from the database
                Note: Currently returns items from fake_items_db for demonstration
    
    Raises:
        ValidationError: If query parameters don't match expected types
    
    HTTP Status Codes:
        - 200: Successfully retrieved users
        - 422: Invalid query parameters (automatic FastAPI validation)
    
    Example Requests:
        ```bash
        # Get all users (first 100)
        curl "http://localhost:8000/users/"
        
        # Search for users
        curl "http://localhost:8000/users/?q=admin"
        
        # Pagination - skip first 5 users, get next 10
        curl "http://localhost:8000/users/?skip=5&limit=10"
        
        # Combined search and pagination
        curl "http://localhost:8000/users/?q=john&skip=0&limit=25"
        ```
    
    Example Responses:
        ```json
        // Basic request
        {"items": [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]}
        
        // With search query
        {"q": "admin", "items": [{"item_name": "Foo"}, {"item_name": "Bar"}]}
        
        // With pagination
        {"items": [{"item_name": "Baz"}]}
        ```
    
    Dependency Syntax Comparison:
        - Explicit: `Depends(CommonQueryParams)` - clearly states the dependency class
        - Shortcut: `Depends()` - FastAPI infers the class from type annotation
        - Both approaches are functionally equivalent
        - Explicit syntax is more verbose but clearer for complex applications
        - Shortcut syntax is more concise and commonly used
    
    When to Use Explicit Syntax:
        - When the dependency class differs from the type annotation
        - For better code readability in complex applications
        - When working with dependency inheritance or polymorphism
        - For explicit documentation of dependency relationships
        - In larger teams where clarity is preferred over brevity
    
    Performance Considerations:
        - Same performance characteristics as the items endpoint
        - Memory-based pagination not suitable for production
        - Consider implementing database-level user queries
        - Add proper indexing for user search functionality
    
    Security Notes:
        - User data requires additional security considerations
        - Implement proper authentication for user endpoints
        - Add authorization checks for user data access
        - Consider PII (Personally Identifiable Information) protection
        - Implement audit logging for user data access
    
    Production Enhancements:
        - Replace with actual user database queries
        - Add user-specific authentication and authorization
        - Implement proper user search with relevant fields
        - Add user filtering capabilities (active, role, etc.)
        - Include user metadata in responses (total users, page info)
        - Consider implementing user caching strategies
    
    Future Improvements:
        - Add user role-based filtering
        - Implement advanced search with multiple criteria
        - Add sorting capabilities (by name, creation date, etc.)
        - Include user profile information in responses
        - Add export functionality for user lists
    """
    # TODO: Create response dict, add q if provided, slice fake_items_db
    response = {}
    if commons.q:
        response["q"] = commons.q
    response["items"] = fake_items_db[commons.skip : commons.skip + commons.limit]
    return response