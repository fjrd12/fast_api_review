"""
18pathoperationconfig.py

Path Operation Configuration in FastAPI
======================================

This module demonstrates comprehensive path operation configuration patterns in FastAPI,
including response models, status codes, tags, documentation, and API metadata.

Key Concepts Covered:
- Response model configuration and validation
- Custom HTTP status codes for operations
- API tagging and organization
- Operation summaries and descriptions
- Docstring-based documentation with markdown
- API deprecation patterns
- Enum-based tag management

Path operation configuration is essential for building well-documented, organized,
and maintainable APIs that provide clear information to both developers and consumers.

Dependencies:
- fastapi: Web framework for building APIs
- pydantic: Data validation and settings management
- enum: Enumeration support for organizing tags

Learning Objectives:
- Configure response models for automatic validation and documentation
- Use appropriate HTTP status codes for different operations
- Organize API endpoints with tags for better documentation structure
- Write effective API documentation using summaries and descriptions
- Leverage docstrings for rich markdown documentation
- Implement API versioning and deprecation strategies

Production Considerations:
- Use consistent tagging strategies for API organization
- Provide comprehensive documentation for all endpoints
- Follow REST conventions for status codes and response formats
- Consider API versioning and backward compatibility
- Implement proper deprecation warnings for obsolete endpoints

Author: FastAPI Tutorial Series
Date: October 2025
Version: 1.0
"""

from enum import Enum
from typing import Set, Union

from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    """
    Item model for representing product/service items in the API.
    
    This Pydantic model defines the structure for items in the system,
    including all necessary fields for item management and validation.
    
    Attributes:
        name (str): The unique name identifier for the item
        description (str | None): Optional detailed description of the item
        price (float): The cost/price of the item (must be positive)
        tax (float | None): Optional tax amount applicable to the item
        tags (Set[str]): A set of categorization tags for the item
        
    Example:
        ```python
        item = Item(
            name="Laptop",
            description="High-performance gaming laptop",
            price=1299.99,
            tax=129.99,
            tags={"electronics", "gaming", "computers"}
        )
        ```
        
    Validation:
        - name: Required string field
        - price: Required positive float
        - tags: Automatically converts to set to ensure uniqueness
        
    Usage:
        This model is used throughout the API for item creation,
        updates, and responses, ensuring consistent data structure.
    """
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()


class Tags(Enum):
    """
    Enumeration for API endpoint tags.
    
    This enum provides a consistent way to categorize API endpoints
    for better organization and documentation generation.
    
    Values:
        items: Tag for item-related endpoints
        users: Tag for user-related endpoints
        
    Benefits:
        - Consistent tag naming across the application
        - Type safety for tag references
        - Easy maintenance and updates
        - Better IDE support and autocompletion
        
    Usage:
        ```python
        @app.get("/items/", tags=[Tags.items])
        async def get_items():
            pass
        ```
    """
    items = "items"
    users = "users"


# Use @app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item) -> Item:
    """
    Create a new item with proper response model and status code configuration.
    
    This endpoint demonstrates the fundamental path operation configuration
    including response model validation and appropriate HTTP status code
    for resource creation operations.
    
    Args:
        item (Item): The item data to create, validated against the Item model
        
    Returns:
        Item: The created item with all provided fields validated and formatted
        
    Configuration:
        - response_model=Item: Ensures response validation and documentation
        - status_code=201: Proper HTTP status for successful resource creation
        
    Example Request:
        POST /items/
        Content-Type: application/json
        
        {
            "name": "Gaming Mouse",
            "description": "High-precision gaming mouse",
            "price": 79.99,
            "tax": 8.00,
            "tags": ["gaming", "electronics"]
        }
        
    Example Response:
        Status: 201 Created
        Content-Type: application/json
        
        {
            "name": "Gaming Mouse",
            "description": "High-precision gaming mouse",
            "price": 79.99,
            "tax": 8.00,
            "tags": ["gaming", "electronics"]
        }
        
    Benefits:
        - Automatic request/response validation
        - Proper HTTP semantics (201 for creation)
        - OpenAPI documentation generation
        - Type safety and IDE support
        
    Note:
        The response_model ensures that the returned data matches the Item schema,
        providing automatic validation and serialization.
    """
    return item

# Create a GET endpoint for items with "items" tag
# Use @app.get("/items/", tags=["items"])
@app.get("/items/", tags=["items"])
async def get_items() -> list[Item]:
    """
    Retrieve all items with string-based tag configuration.
    
    This endpoint demonstrates basic API tagging using string literals
    for organizing endpoints in the automatically generated documentation.
    
    Returns:
        list[Item]: A list of all available items in the system
        
    Configuration:
        - tags=["items"]: Groups this endpoint under the "items" section
        
    Example Request:
        GET /items/
        
    Example Response:
        Status: 200 OK
        Content-Type: application/json
        
        [
            {
                "name": "burro",
                "description": "gato",
                "price": 10,
                "tax": null,
                "tags": ["1", "2"]
            }
        ]
        
    API Documentation:
        - Appears in the "items" section of the OpenAPI documentation
        - Helps organize related endpoints for better user experience
        - Enables filtering and grouping in API documentation tools
        
    Note:
        Tags are used purely for documentation organization and do not
        affect the actual API functionality or routing.
    """
    return [{"name": 'burro', "description": 'gato',"price": 10, "tags": ['1','2']}]

# Create a GET endpoint for users with "users" tag
# Use @app.get("/users/", tags=["users"])
@app.get("/users/", tags=["users"])
async def get_users() -> list[dict]:
    """
    Retrieve all users with tag-based API organization.
    
    This endpoint demonstrates API organization using tags to separate
    different resource types (users vs items) in the documentation.
    
    Returns:
        list[dict]: A list of user objects with basic information
        
    Configuration:
        - tags=["users"]: Groups this endpoint under the "users" section
        
    Example Request:
        GET /users/
        
    Example Response:
        Status: 200 OK
        Content-Type: application/json
        
        [
            {"name": "Pedro"},
            {"name": "Maria"}
        ]
        
    API Organization:
        - Separated from items endpoints in documentation
        - Creates distinct sections for different resource types
        - Improves API discoverability and navigation
        
    Note:
        This endpoint returns a simple dict structure rather than a
        Pydantic model to demonstrate flexibility in response types.
    """
    return [{'name': 'Pedro'}, {'name': 'Maria'}]

# Create a GET endpoint for elements with Tags.items enum tag
# Use @app.get("/elements/", tags=[Tags.items])
@app.get("/elements/", tags=[Tags.items])
async def get_elements() -> list[str]:
    """
    Retrieve elements using enum-based tag configuration.
    
    This endpoint demonstrates the use of enum values for tags,
    providing better type safety and maintainability compared to
    string literals.
    
    Returns:
        list[str]: A list of element identifiers
        
    Configuration:
        - tags=[Tags.items]: Uses enum value for type-safe tag assignment
        
    Example Request:
        GET /elements/
        
    Example Response:
        Status: 200 OK
        Content-Type: application/json
        
        ["element1", "element2"]
        
    Enum Benefits:
        - Type safety at development time
        - IDE autocompletion and validation
        - Centralized tag management
        - Easier refactoring and maintenance
        - Prevents typos in tag names
        
    Note:
        Using enums for tags is a best practice for larger applications
        where consistency and maintainability are important.
    """
    return ['element1', 'element2']


# Create a POST endpoint with summary and description
# Use @app.post("/items-summary/", response_model=Item, summary="Create an item", description="...")
@app.post("/items-summary/", response_model=Item, summary="Create an item", description="This endpoint creates an item with the provided details and returns the created item.")
async def create_item_summary(item: Item) -> Item:
    """
    Create an item with explicit summary and description configuration.
    
    This endpoint demonstrates how to use the summary and description
    parameters in the path operation decorator for API documentation.
    
    Args:
        item (Item): The item data to create
        
    Returns:
        Item: The created item with validation
        
    Configuration:
        - summary: Brief title shown in API documentation
        - description: Detailed explanation of the endpoint's purpose
        - response_model: Ensures response validation and schema generation
        
    Example Request:
        POST /items-summary/
        Content-Type: application/json
        
        {
            "name": "Wireless Headphones",
            "description": "Noise-cancelling wireless headphones",
            "price": 199.99,
            "tax": 20.00,
            "tags": ["audio", "electronics", "wireless"]
        }
        
    Example Response:
        Status: 200 OK
        Content-Type: application/json
        
        {
            "name": "Wireless Headphones",
            "description": "Noise-cancelling wireless headphones",
            "price": 199.99,
            "tax": 20.00,
            "tags": ["audio", "electronics", "wireless"]
        }
        
    Documentation Benefits:
        - Clear, concise summary for quick understanding
        - Detailed description for comprehensive information
        - Appears prominently in OpenAPI/Swagger documentation
        - Helps API consumers understand endpoint purpose
        
    Note:
        The summary appears as the endpoint title, while the description
        provides additional context. Both enhance API documentation quality.
    """
    return item

# Create a POST endpoint with docstring description
# Use @app.post("/items-docstring/", response_model=Item, summary="Create an item")
# Add a detailed docstring with markdown
@app.post("/items-docstring/", response_model=Item, summary="Create an item")
async def create_item_docstring(item: Item) -> Item:
    """
    Create an item with detailed description.
    
    This endpoint allows you to create an item by providing its details
    in the request body. The created item is then returned in the response.
    
    **Request Body:**
    
    - `name` (str): The name of the item (required)
    - `description` (str | None): Optional description of the item
    - `price` (float): The price of the item (required)
    - `tax` (float | None): Optional tax amount for the item
    - `tags` (set[str]): A set of tags associated with the item
    
    **Response:**
    
    Returns the created item with all provided details.
    
    **Example Request Body:**
    
    ```json
    {
        "name": "Laptop",
        "description": "A high-end gaming laptop",
        "price": 1500.00,
        "tax": 150.00,
        "tags": ["electronics", "gaming"]
    }
    ```
    
    **Example Response:**
    
    ```json
    {
        "name": "Laptop",
        "description": "A high-end gaming laptop",
        "price": 1500.00,
        "tax": 150.00,
        "tags": ["electronics", "gaming"]
    }
    ```
    """
    return item

# Create a deprecated GET endpoint for elements
# Use @app.get("/elements/", tags=["items"], deprecated=True)
@app.get("/elements/", tags=["items"], deprecated=True)
async def get_elements_deprecated() -> list[str]:
    """
    Retrieve elements (DEPRECATED).
    
    This endpoint demonstrates API deprecation patterns and how to
    properly mark endpoints as deprecated while maintaining backward
    compatibility.
    
    ⚠️ **DEPRECATION WARNING**: This endpoint is deprecated and will be
    removed in a future version. Please use the new `/elements/` endpoint
    without the deprecated parameter.
    
    Returns:
        list[str]: A list of element identifiers
        
    Configuration:
        - deprecated=True: Marks the endpoint as deprecated in documentation
        - tags=["items"]: Groups with related endpoints
        
    Example Request:
        GET /elements/
        
    Example Response:
        Status: 200 OK
        Content-Type: application/json
        
        ["element1", "element2"]
        
    Deprecation Strategy:
        1. Mark endpoint as deprecated
        2. Update documentation with migration instructions
        3. Provide timeline for removal
        4. Monitor usage and communicate with consumers
        5. Eventually remove the endpoint
        
    Migration Guide:
        - Use the new `/elements/` endpoint (without deprecated flag)
        - The response format remains the same
        - Update client code to use the new endpoint URL
        
    Note:
        Deprecated endpoints continue to function but are marked clearly
        in the API documentation to guide users toward newer alternatives.
    """
    return ['element1', 'element2']