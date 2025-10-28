"""
Response Model - Return Type

This module demonstrates how to declare response models using return type annotations 
and the response_model parameter in FastAPI. Response models define the structure 
of data that your API endpoints return, enabling automatic validation, serialization, 
and API documentation generation.

Key concepts covered:
- Using return type annotations (-> Type) to declare response models
- Combining response_model parameter with return type annotations
- Returning Pydantic models from endpoints
- Returning lists of Pydantic models
- Automatic JSON serialization based on response models

The response_model parameter and return type annotations work together to:
1. Validate the response data against the specified model
2. Serialize the response to JSON automatically
3. Generate accurate OpenAPI documentation
4. Provide type hints for better IDE support
"""

from typing import Any
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    """
    Item model representing a product or service.
    
    This Pydantic model defines the structure for items in our API,
    including validation rules and default values.
    
    Attributes:
        name (str): The name of the item (required)
        description (str | None): Optional description of the item
        price (float): The price of the item (required)
        tax (float | None): Optional tax amount for the item
        tags (list[str]): List of tags associated with the item (defaults to empty list)
    
    Example:
        >>> item = Item(name="Laptop", price=999.99, description="Gaming laptop")
        >>> print(item.name)
        Laptop
    """
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []

#Create a POST endpoint at "/items/" that accepts an Item and returns it
# Use return type annotation -> Item to declare the response model
@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Item:
    """
    Create a new item and return it.
    
    This endpoint demonstrates how to use return type annotations (-> Item)
    combined with the response_model parameter to declare what the endpoint returns.
    The response_model ensures the returned data matches the Item model structure.
    
    Args:
        item (Item): The item data to create, validated against the Item model
    
    Returns:
        Item: The created item with the same data as input
    
    Response Model:
        The response will be automatically serialized to JSON following the Item model structure:
        - name: string (required)
        - description: string or null (optional)
        - price: number (required)
        - tax: number or null (optional)
        - tags: array of strings (optional, defaults to empty array)
    
    Example Request Body:
        {
            "name": "Laptop",
            "description": "Gaming laptop",
            "price": 999.99,
            "tax": 99.99,
            "tags": ["electronics", "gaming"]
        }
    
    Example Response:
        {
            "name": "Laptop",
            "description": "Gaming laptop", 
            "price": 999.99,
            "tax": 99.99,
            "tags": ["electronics", "gaming"]
        }
    """
    return item

#Create a GET endpoint at "/items/" that returns a list of items
# Use return type annotation -> list[Item] to declare the response model
# Return this sample data:
# [
#     {"name": "Portal Gun", "price": 42.0},
#     {"name": "Plumbus", "price": 32.0},
# ]
@app.get("/items/", response_model=list[Item])
async def read_items() -> list[Item]:
    """
    Retrieve a list of all items.
    
    This endpoint demonstrates how to return a list of Pydantic models using
    return type annotation (-> list[Item]) combined with response_model=list[Item].
    The response model ensures each item in the list follows the Item model structure.
    
    Returns:
        list[Item]: A list of Item objects with sample data
    
    Response Model:
        The response will be a JSON array where each element follows the Item model:
        - Each item contains: name, description, price, tax, tags
        - Missing optional fields (description, tax) will be null
        - Missing tags field will default to empty array
    
    Example Response:
        [
            {
                "name": "Portal Gun",
                "description": null,
                "price": 42.0,
                "tax": null,
                "tags": []
            },
            {
                "name": "Plumbus", 
                "description": null,
                "price": 32.0,
                "tax": null,
                "tags": []
            }
        ]
    
    Note:
        The sample data returned contains only name and price fields.
        FastAPI automatically fills in missing optional fields with their default values
        (None for description and tax, empty list for tags) based on the Item model.
    """
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]