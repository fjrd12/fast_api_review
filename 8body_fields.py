"""
FastAPI Body Fields - Pydantic Field Validation and Metadata

This module demonstrates how to add validation and metadata to Pydantic model fields
using the Field() function. Field validation provides fine-grained control over
data validation, constraints, and documentation for individual model attributes.

Key concepts covered:
- Pydantic Field() function for advanced field validation
- Numeric constraints (gt, ge, lt, le) for number fields
- String constraints (max_length, min_length) for text fields
- Field metadata (title, description) for API documentation
- Combining Field validation with Body embedding
- Custom validation messages and constraints

Run with: fastapi dev 8body_fields.py
"""

from typing import Union
from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="Body Fields Validation Demo",
    description="A FastAPI application demonstrating Pydantic Field validation and metadata",
    version="1.0.0"
)


class Item(BaseModel):
    """
    Pydantic model with Field validation and metadata.
    
    This model demonstrates various Field() validation techniques including
    numeric constraints, string length limits, and documentation metadata.
    Each field showcases different validation patterns commonly used in APIs.
    
    Attributes:
        name (str): The name of the item (required, no validation)
        description (Union[str, None]): Optional description with length limit and metadata
        price (float): Price with numeric constraint (must be > 0)
        tax (Union[float, None]): Optional tax amount (no validation)
        
    Field Validation Features:
        - description: max_length=300, custom title for documentation
        - price: gt=0 (greater than zero), custom description
        
    Example JSON:
        {
            "name": "Laptop",
            "description": "High-performance gaming laptop",
            "price": 999.99,
            "tax": 99.99
        }
    """
    name: str
    description: Union[str, None] = Field(
        default=None, 
        title="The description of the item", 
        max_length=300
    )
    price: float = Field(
        gt=0, 
        description="The price must be greater than zero"
    )
    tax: Union[float, None] = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(embed=True)) -> dict:
    """
    Update an item with Field-validated request body.
    
    This endpoint demonstrates the combination of Pydantic Field validation
    with Body embedding. The request body is validated according to the
    Field constraints defined in the Item model, and validation errors
    are automatically returned if constraints are violated.
    
    Args:
        item_id (int): The ID of the item to update (path parameter)
        item (Item): Item data with Field validation, embedded using Body(embed=True)
        
    Returns:
        dict: A dictionary containing the item_id and the validated item data
        
    Field Validation Applied:
        - name: Required string (no additional validation)
        - description: Optional string, max 300 characters
        - price: Required float, must be > 0
        - tax: Optional float (no validation)
        
    Request Body Structure (due to embed=True):
        {
            "item": {
                "name": "string",
                "description": "string (optional, max 300 chars)",
                "price": 0.0 (must be > 0),
                "tax": 0.0 (optional)
            }
        }
        
    Example Request:
        PUT /items/123
        Content-Type: application/json
        
        {
            "item": {
                "name": "Gaming Laptop",
                "description": "High-end gaming laptop with RTX graphics",
                "price": 1299.99,
                "tax": 130.00
            }
        }
        
    Example Response:
        {
            "item_id": 123,
            "item": {
                "name": "Gaming Laptop",
                "description": "High-end gaming laptop with RTX graphics",
                "price": 1299.99,
                "tax": 130.0
            }
        }
        
    Validation Errors (422):
        - price <= 0: "ensure this value is greater than 0"
        - description > 300 chars: "ensure this value has at most 300 characters"
        - missing name: "field required"
        - missing price: "field required"
        
    Field Validation Benefits:
        - Automatic validation before function execution
        - Detailed error messages for constraint violations
        - Enhanced API documentation with field metadata
        - Type safety and data integrity
        - Consistent validation across all endpoints using the model
        
    Note:
        Body(embed=True) ensures the Item model is wrapped in an "item" key
        in the request JSON, providing consistent structure even with single models.
    """
    return {"item_id": item_id, "item": item}