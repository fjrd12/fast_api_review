"""
FastAPI Query Parameters Example

This module demonstrates the use of query parameters in FastAPI applications.
Query parameters are optional parameters that appear after the '?' in a URL
and are separated by '&' characters.

Key concepts covered:
- Basic query parameters with default values
- Optional query parameters
- Combining path and query parameters
- Type validation for query parameters
- Parameter ordering and precedence

Run with: fastapi dev query_parameters.py
"""

from fastapi import FastAPI
from typing import Union

app = FastAPI(
    title="Query Parameters Demo",
    description="A FastAPI application demonstrating query parameters usage",
    version="1.0.0"
)


@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10) -> dict:
    """
    Get a list of items with pagination support.
    
    This endpoint demonstrates basic query parameters with default values.
    Both parameters are optional and will use default values if not provided.
    
    Args:
        skip (int, optional): Number of items to skip. Defaults to 0.
        limit (int, optional): Maximum number of items to return. Defaults to 10.
        
    Returns:
        dict: A dictionary containing the skip and limit values
        
    Examples:
        GET /items/ -> {"skip": 0, "limit": 10}
        GET /items/?skip=5 -> {"skip": 5, "limit": 10}
        GET /items/?limit=20 -> {"skip": 0, "limit": 20}
        GET /items/?skip=10&limit=5 -> {"skip": 10, "limit": 5}
        
    Note:
        FastAPI automatically validates that skip and limit are integers.
        If non-integer values are provided, a 422 validation error is returned.
    """
    return {"skip": skip, "limit": limit}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None) -> dict:
    """
    Get a specific item by ID with optional search query.
    
    This endpoint demonstrates combining path parameters with query parameters.
    The item_id is required (path parameter) while q is optional (query parameter).
    
    Args:
        item_id (int): The ID of the item to retrieve (path parameter)
        q (Union[str, None], optional): Optional search query string. Defaults to None.
        
    Returns:
        dict: A dictionary containing the item_id and query string
        
    Raises:
        422 Validation Error: If item_id cannot be converted to an integer
        
    Examples:
        GET /items/42 -> {"item_id": 42, "q": null}
        GET /items/42?q=search -> {"item_id": 42, "q": "search"}
        GET /items/42?q=hello%20world -> {"item_id": 42, "q": "hello world"}
        GET /items/abc -> 422 Validation Error (invalid item_id)
        
    Note:
        - The path parameter (item_id) is always required
        - Query parameters can be omitted and will use their default values
        - URL encoding is automatically handled (e.g., %20 becomes space)
    """
    return {"item_id": item_id, "q": q}
