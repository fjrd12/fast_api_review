"""
FastAPI Request Body Example

This module demonstrates how to handle request bodies in FastAPI applications
using Pydantic models for data validation and serialization.

Key concepts covered:
- Pydantic BaseModel for data validation
- Request body handling with POST and PUT methods
- Optional fields with default values
- Type hints and automatic validation
- Model serialization with model_dump()
- Combining path parameters with request bodies

Run with: fastapi dev request_body.py
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union

app = FastAPI(
    title="Request Body Demo",
    description="A FastAPI application demonstrating request body handling with Pydantic models",
    version="1.0.0"
)


class Item(BaseModel):
    """
    Pydantic model representing an item with validation rules.
    
    This model defines the structure and validation for item data
    that will be sent in request bodies.
    
    Attributes:
        name (str): The name of the item (required)
        description (Union[str, None]): Optional description of the item
        price (float): The price of the item (required, must be a number)
        tax (Union[float, None]): Optional tax amount for the item
        
    Example:
        {
            "name": "Laptop",
            "description": "Gaming laptop",
            "price": 999.99,
            "tax": 99.99
        }
    """
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@app.post("/items/")
async def create_item(item: Item) -> Item:
    """
    Create a new item.
    
    This endpoint demonstrates basic request body handling with a Pydantic model.
    The request body is automatically validated against the Item model schema.
    
    Args:
        item (Item): The item data from the request body
        
    Returns:
        Item: The same item data that was received (echo response)
        
    Raises:
        422 Validation Error: If the request body doesn't match the Item schema
        
    Example Request:
        POST /items/
        Content-Type: application/json
        
        {
            "name": "Laptop",
            "description": "Gaming laptop",
            "price": 999.99,
            "tax": 99.99
        }
        
    Example Response:
        {
            "name": "Laptop",
            "description": "Gaming laptop",
            "price": 999.99,
            "tax": 99.99
        }
        
    Note:
        - FastAPI automatically validates the JSON against the Pydantic model
        - Missing required fields (name, price) will cause a 422 error
        - Optional fields (description, tax) can be omitted
    """
    return item


@app.post("/items/{item_id}")
async def update_item(item_id: int, item: Item) -> dict:
    """
    Update an existing item by ID.
    
    This endpoint demonstrates combining path parameters with request bodies.
    It shows how to merge path parameter data with request body data using
    dictionary unpacking with model_dump().
    
    Args:
        item_id (int): The ID of the item to update (path parameter)
        item (Item): The updated item data from the request body
        
    Returns:
        dict: A dictionary containing the item_id and all item fields
        
    Raises:
        422 Validation Error: If item_id is not an integer or request body is invalid
        
    Example Request:
        POST /items/123
        Content-Type: application/json
        
        {
            "name": "Updated Laptop",
            "description": "High-end gaming laptop",
            "price": 1299.99,
            "tax": 129.99
        }
        
    Example Response:
        {
            "item_id": 123,
            "name": "Updated Laptop",
            "description": "High-end gaming laptop",
            "price": 1299.99,
            "tax": 129.99
        }
        
    Note:
        - **item.model_dump() unpacks all model fields into the response dict
        - This creates a flat structure combining path and body parameters
        - model_dump() converts the Pydantic model to a Python dictionary
        - The ** operator spreads the dictionary key-value pairs
    """
    return {"item_id": item_id, **item.model_dump()}