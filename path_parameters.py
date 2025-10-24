"""
FastAPI Path Parameters Example

This module demonstrates the use of path parameters in FastAPI applications.
Path parameters are variables in the URL path that can be captured and used
in endpoint functions.

Key concepts covered:
- Basic path parameters
- Type hints for path parameters
- Order of endpoint definitions
- Path parameter validation

Run with: fastapi dev path_parameters.py
"""

from fastapi import FastAPI

app = FastAPI(
    title="Path Parameters Demo",
    description="A simple FastAPI application demonstrating path parameters",
    version="1.0.0"
)


@app.get("/items/{item_id}")
async def get_item(item_id: str) -> dict:
    """
    Get an item by its ID (as string).
    
    This endpoint demonstrates basic path parameter usage where the parameter
    is treated as a string by default.
    
    Args:
        item_id (str): The ID of the item to retrieve
        
    Returns:
        dict: A dictionary containing the item_id
        
    Example:
        GET /items/foo -> {"item_id": "foo"}
        GET /items/123 -> {"item_id": "123"}
    """
    return {"item_id": item_id}


@app.get("/items/{item_id}/typed")
async def get_typed(item_id: int) -> dict:
    """
    Get an item by its ID (as integer).
    
    This endpoint demonstrates typed path parameters. FastAPI will automatically
    validate that the path parameter can be converted to an integer.
    
    Args:
        item_id (int): The ID of the item to retrieve (must be a valid integer)
        
    Returns:
        dict: A dictionary containing the item_id as an integer
        
    Raises:
        422 Validation Error: If item_id cannot be converted to an integer
        
    Example:
        GET /items/123/typed -> {"item_id": 123}
        GET /items/abc/typed -> 422 Validation Error
    """
    return {"item_id": item_id}


@app.get("/users/me")
async def get_myself() -> dict:
    """
    Get the current user's information.
    
    This endpoint demonstrates a fixed path without parameters. Note that this
    endpoint is defined after the parameterized endpoints but with a specific
    path. FastAPI matches the most specific path first.
    
    Returns:
        dict: Information about the current user
        
    Example:
        GET /users/me -> {"user_id": "The current user"}
    """
    return {"user_id": "The current user"}


@app.get("/users/{user_id}")
async def get_user(user_id: str) -> dict:
    """
    Get a specific user by their ID.
    
    This endpoint demonstrates path parameters with user resources. It accepts
    any string as a user ID and returns it in the response. This endpoint is
    defined after /users/me, which is important for proper routing - FastAPI
    matches the most specific routes first.
    
    Args:
        user_id (str): The ID of the user to retrieve
        
    Returns:
        dict: A dictionary containing the user_id
        
    Example:
        GET /users/john -> {"user_id": "john"}
        GET /users/123 -> {"user_id": "123"}
        
    Note:
        This route is defined after /users/me to avoid conflicts.
        If defined before, /users/me would be interpreted as user_id="me".
    """
    return {"user_id": user_id}
