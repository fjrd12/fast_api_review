"""
FastAPI Body Multiple Parameters - Complete Tutorial

This module demonstrates advanced FastAPI concepts for handling multiple parameters
including path parameters, query parameters, and multiple request body parameters.
Following the official FastAPI tutorial covering all 5 key concepts.

Key concepts covered:
- Mixing path, query, and body parameters
- Multiple body parameters in a single endpoint
- Singular values in body using Body()
- Combining multiple body parameters with query parameters
- Embedding single body parameters

Run with: fastapi dev 7bodymultipleparameters.py
"""

from typing import Union
from fastapi import FastAPI, Path, Body
from pydantic import BaseModel

app = FastAPI(
    title="Multiple Body Parameters Demo",
    description="A FastAPI application demonstrating advanced parameter handling with multiple body parameters",
    version="1.0.0"
)

# Pydantic models for request bodies
class Item(BaseModel):
    """
    Pydantic model representing an item with optional fields.
    
    This model demonstrates the use of Union types for optional fields
    that can be either a specific type or None.
    
    Attributes:
        name (str): The name of the item (required)
        description (Union[str, None]): Optional description of the item
        price (float): The price of the item (required)
        tax (Union[float, None]): Optional tax amount for the item
    """
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


class User(BaseModel):
    """
    Pydantic model representing a user with optional full name.
    
    This model demonstrates a simple user structure with both
    required and optional fields.
    
    Attributes:
        username (str): The username of the user (required)
        full_name (Union[str, None]): Optional full name of the user
    """
    username: str
    full_name: Union[str, None] = None


@app.put("/items/{item_id}/basic")
async def update_item_basic(
    item_id: int = Path(title="The Id of the item to get", ge=0, le=1000), 
    q: Union[str, None] = None, 
    item: Union[Item, None] = None
) -> dict:
    """
    Mix path, query, and body parameters in a single endpoint.
    
    This endpoint demonstrates how to combine different parameter types:
    - Path parameter with validation constraints
    - Optional query parameter
    - Optional request body parameter
    
    Args:
        item_id (int): The ID of the item (path parameter, 0-1000)
        q (Union[str, None], optional): Optional query parameter
        item (Union[Item, None], optional): Optional item data in request body
        
    Returns:
        dict: A dictionary containing item_id and conditionally q and item
        
    Example Request:
        PUT /items/123/basic?q=search
        Content-Type: application/json
        
        {
            "name": "Laptop",
            "price": 999.99
        }
        
    Example Response:
        {
            "item_id": 123,
            "q": "search",
            "item": {
                "name": "Laptop",
                "description": null,
                "price": 999.99,
                "tax": null
            }
        }
    """
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results


@app.put("/items/{item_id}")
async def get_multiple_body_params(item_id: int, item: Item, user: User) -> dict:
    """
    Handle multiple body parameters in a single endpoint.
    
    This endpoint demonstrates the main concept of having multiple Pydantic models
    as request body parameters. FastAPI automatically combines them into a single
    JSON request body with separate sections for each model.
    
    Args:
        item_id (int): The ID of the item (path parameter)
        item (Item): Item data from request body
        user (User): User data from request body
        
    Returns:
        dict: A dictionary containing all parameters
        
    Expected Request Body Structure:
        {
            "item": {
                "name": "string",
                "description": "string or null",
                "price": 0.0,
                "tax": 0.0 or null
            },
            "user": {
                "username": "string",
                "full_name": "string or null"
            }
        }
        
    Example Request:
        PUT /items/456
        Content-Type: application/json
        
        {
            "item": {
                "name": "Gaming Mouse",
                "price": 59.99,
                "tax": 5.99
            },
            "user": {
                "username": "john_doe",
                "full_name": "John Doe"
            }
        }
    """
    return {
        "item_id": item_id,
        "item": item,
        "user": user
    }


@app.put("/items/{item_id}/importance")
async def get_unique_body(item_id: int, item: Item, user: User, importance: int = Body()) -> dict:
    """
    Include singular values in the request body using Body().
    
    This endpoint demonstrates how to include individual values (not just Pydantic models)
    in the request body by using Body(). This allows mixing complex models with
    simple scalar values in the same request body.
    
    Args:
        item_id (int): The ID of the item (path parameter)
        item (Item): Item data from request body
        user (User): User data from request body
        importance (int): Importance level as a singular value in body using Body()
        
    Returns:
        dict: A dictionary containing all parameters
        
    Expected Request Body Structure:
        {
            "item": { ... },
            "user": { ... },
            "importance": 5
        }
        
    Example Request:
        PUT /items/789/importance
        Content-Type: application/json
        
        {
            "item": {
                "name": "Mechanical Keyboard",
                "price": 149.99
            },
            "user": {
                "username": "jane_smith"
            },
            "importance": 8
        }
        
    Note:
        Without Body(), importance would be treated as a query parameter.
        Body() forces it to be included in the request body JSON.
    """
    return {
        "item_id": item_id,
        "item": item,
        "user": user,
        "importance": importance
    }


@app.put("/items/{item_id}/full")
async def get_full_body_params(
    item_id: int, 
    item: Item, 
    user: User, 
    importance: int = Body(gt=0), 
    q: str | None = None
) -> dict:
    """
    Combine multiple body parameters with query parameters and validation.
    
    This endpoint demonstrates the most complex scenario: combining multiple
    body parameters, singular body values with validation, and optional
    query parameters in a single endpoint.
    
    Args:
        item_id (int): The ID of the item (path parameter)
        item (Item): Item data from request body
        user (User): User data from request body
        importance (int): Importance level with validation (Body, must be > 0)
        q (str | None, optional): Optional query parameter
        
    Returns:
        dict: A dictionary containing all parameters, conditionally including q
        
    Expected Request Body Structure:
        {
            "item": { ... },
            "user": { ... },
            "importance": 5
        }
        
    Example Request:
        PUT /items/999/full?q=urgent
        Content-Type: application/json
        
        {
            "item": {
                "name": "Monitor",
                "description": "4K Gaming Monitor",
                "price": 399.99,
                "tax": 40.00
            },
            "user": {
                "username": "admin",
                "full_name": "System Administrator"
            },
            "importance": 10
        }
        
    Validation:
        - importance must be > 0 (Body(gt=0))
        - Will return 422 if importance <= 0
    """
    results = {
        "item_id": item_id,
        "item": item,
        "user": user,
        "importance": importance
    }
    if q:
        results.update({"q": q})
    return results


@app.put("/items/{item_id}/embed")
async def get_embed_body(item_id: int, item: Item = Body(embed=True)) -> dict:
    """
    Embed a single body parameter using Body(embed=True).
    
    This endpoint demonstrates how to force a single Pydantic model to be
    embedded in the request body JSON structure. Normally, a single body
    parameter would be at the root level, but embed=True wraps it in an object.
    
    Args:
        item_id (int): The ID of the item (path parameter)
        item (Item): Item data embedded in request body using Body(embed=True)
        
    Returns:
        dict: A dictionary containing item_id and the embedded item
        
    Without embed=True, expected structure would be:
        {
            "name": "string",
            "description": "string",
            "price": 0.0,
            "tax": 0.0
        }
        
    With embed=True, expected structure is:
        {
            "item": {
                "name": "string",
                "description": "string",
                "price": 0.0,
                "tax": 0.0
            }
        }
        
    Example Request:
        PUT /items/111/embed
        Content-Type: application/json
        
        {
            "item": {
                "name": "Wireless Headphones",
                "description": "Noise-cancelling headphones",
                "price": 199.99,
                "tax": 20.00
            }
        }
        
    Note:
        embed=True is useful when you want consistent JSON structure
        across endpoints, even with single body parameters.
    """
    return {"item_id": item_id, "item": item}