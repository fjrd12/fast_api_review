"""
20Bodyupdates.py

Body Updates in FastAPI
======================

This module demonstrates comprehensive body update patterns in FastAPI applications,
including full updates (PUT) and partial updates (PATCH) with proper data handling
and validation techniques.

Key Concepts Covered:
- PUT requests for complete resource replacement
- PATCH requests for partial resource updates
- Pydantic model validation and data conversion
- exclude_unset parameter for partial updates
- model_dump() and model_validate() methods
- copy() method for safe model updates
- HTTP semantics for different update operations

Body updates are essential for building REST APIs that allow clients to modify
existing resources either completely or partially, following HTTP conventions.

Dependencies:
- fastapi: Web framework for building APIs
- pydantic: Data validation and model management
- typing: Type hints for optional fields

Learning Objectives:
- Understand the difference between PUT and PATCH operations
- Learn to handle complete vs partial resource updates
- Practice Pydantic model manipulation and validation
- Implement proper HTTP semantics for update operations
- Handle optional fields and exclude_unset functionality

Production Considerations:
- Always validate data before updating resources
- Use appropriate HTTP methods (PUT for full, PATCH for partial)
- Implement proper error handling for missing resources
- Consider data consistency and atomic operations
- Log update operations for audit trails

Author: FastAPI Tutorial Series
Date: October 2025
Version: 1.0
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Item(BaseModel):
    """
    Item model for demonstrating update operations with optional fields.
    
    This Pydantic model defines an item structure with optional fields
    to demonstrate different update patterns (PUT vs PATCH) and how
    to handle partial data updates properly.
    
    Attributes:
        name (str | None): The name of the item (optional for updates)
        description (str | None): Detailed description of the item (optional)
        price (float | None): The price of the item (optional for updates)
        tax (float): Tax amount with default value of 10.5
        
    Design Notes:
        - All fields except tax are optional to support partial updates
        - tax has a default value to demonstrate mixed field types
        - Optional fields enable PATCH operations with exclude_unset
        
    Update Patterns:
        - PUT: All fields should be provided (full replacement)
        - PATCH: Only changed fields need to be provided (partial update)
        
    Example Full Update (PUT):
        ```python
        Item(
            name="Updated Item",
            description="Updated description",
            price=99.99,
            tax=15.0
        )
        ```
        
    Example Partial Update (PATCH):
        ```python
        Item(price=89.99)  # Only update price
        ```
        
    Validation:
        - Pydantic ensures type safety for all fields
        - Optional fields can be None or omitted
        - Default values are applied when fields are not provided
    """
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: float = 10.5

# Simulated database
items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5}
}

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    """
    Retrieve an item by its ID.
    
    This endpoint provides read access to items stored in the simulated database.
    It serves as the foundation for update operations by allowing clients to
    retrieve current item state before modifications.
    
    Args:
        item_id (str): The unique identifier of the item to retrieve
        
    Returns:
        Item: The item data with all fields populated
        
    Raises:
        HTTPException: 404 error if the item_id is not found in the database
        
    Example Request:
        GET /items/foo
        
    Example Response (Success):
        Status: 200 OK
        Content-Type: application/json
        
        {
            "name": "Foo",
            "description": null,
            "price": 50.2,
            "tax": 10.5
        }
        
    Example Response (Error):
        Status: 404 Not Found
        Content-Type: application/json
        
        {
            "detail": "Item not found"
        }
        
    Usage Pattern:
        Typically used before update operations to:
        1. Verify the item exists
        2. Get current values for comparison
        3. Implement optimistic locking patterns
        
    Note:
        This endpoint demonstrates basic CRUD read operation that supports
        the update endpoints by providing current resource state.
    """
    # TODO: Check if item exists, return 404 if not found
    # TODO: Return the item data
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

@app.put("/items/{item_id}", response_model=Item)
async def update_item_with_put(item_id: str, item: Item):
    """
    Update an item completely using PUT method (full replacement).
    
    This endpoint implements the HTTP PUT semantics for complete resource
    replacement. The entire item is replaced with the provided data,
    following REST conventions for full updates.
    
    Args:
        item_id (str): The unique identifier of the item to update
        item (Item): The complete item data to replace the existing item
        
    Returns:
        Item: The updated item data as stored in the database
        
    Raises:
        HTTPException: 404 error if the item_id is not found in the database
        
    HTTP Semantics:
        - PUT replaces the entire resource
        - All fields should be provided in the request body
        - Idempotent operation (multiple calls have same effect)
        - Creates resource if it doesn't exist (not implemented here)
        
    Example Request:
        PUT /items/foo
        Content-Type: application/json
        
        {
            "name": "Updated Foo",
            "description": "Completely updated description",
            "price": 75.0,
            "tax": 12.5
        }
        
    Example Response:
        Status: 200 OK
        Content-Type: application/json
        
        {
            "name": "Updated Foo",
            "description": "Completely updated description",
            "price": 75.0,
            "tax": 12.5
        }
        
    Data Handling:
        1. Validates the incoming Item model using Pydantic
        2. Checks if the item exists in the database
        3. Converts the Pydantic model to dict using model_dump()
        4. Replaces the entire item in the database
        5. Returns the updated item data
        
    Use Cases:
        - Complete item overhaul
        - Resetting all fields to new values
        - Bulk property updates
        - Standardizing item format
        
    Note:
        PUT operations should provide all fields. Missing optional fields
        will be set to their default values or None as defined in the model.
    """
    # TODO: Check if item exists, return 404 if not found
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    # TODO: Convert item to dict using jsonable_encoder and store in database
    items[item_id] = item.model_dump()
    # TODO: Return the encoded item
    return items[item_id]

@app.patch("/items/{item_id}", response_model=Item)
async def update_item_with_patch(item_id: str, item: Item):
    """
    Update an item partially using PATCH method (selective updates).
    
    This endpoint implements the HTTP PATCH semantics for partial resource
    updates. Only the fields provided in the request body are updated,
    while other fields remain unchanged.
    
    Args:
        item_id (str): The unique identifier of the item to update
        item (Item): The partial item data containing only fields to update
        
    Returns:
        Item: The complete updated item data as stored in the database
        
    Raises:
        HTTPException: 404 error if the item_id is not found in the database
        
    HTTP Semantics:
        - PATCH updates only specified fields
        - Unspecified fields remain unchanged
        - Non-idempotent operation (multiple calls may have different effects)
        - More efficient for small changes
        
    Example Request (Update only price):
        PATCH /items/foo
        Content-Type: application/json
        
        {
            "price": 85.0
        }
        
    Example Response:
        Status: 200 OK
        Content-Type: application/json
        
        {
            "name": "Foo",           // unchanged
            "description": null,     // unchanged
            "price": 85.0,          // updated
            "tax": 10.5             // unchanged
        }
        
    Data Handling Process:
        1. Validates the incoming partial Item model using Pydantic
        2. Checks if the item exists in the database
        3. Retrieves and validates the stored item as a Pydantic model
        4. Extracts only the fields that were explicitly set using exclude_unset=True
        5. Creates an updated model by copying the stored model with updates
        6. Stores the updated item back to the database
        7. Returns the complete updated item data
        
    Key Pydantic Methods:
        - model_validate(): Creates Pydantic model from dict data
        - model_dump(exclude_unset=True): Gets only explicitly set fields
        - copy(update=data): Creates new model instance with updates
        
    Use Cases:
        - Single field updates (e.g., just price change)
        - Incremental modifications
        - Preserving unchanged data
        - Efficient bandwidth usage
        - Atomic field updates
        
    Example Scenarios:
        - Update only item price: {"price": 99.99}
        - Change description only: {"description": "New description"}
        - Update multiple fields: {"price": 50.0, "tax": 5.0}
        
    Advantages over PUT:
        - Bandwidth efficient (only send changed fields)
        - Preserves unchanged data automatically
        - Reduces risk of accidental data loss
        - Better for concurrent modifications
        
    Note:
        The exclude_unset=True parameter is crucial for PATCH operations
        as it ensures only explicitly provided fields are updated.
    """
    # TODO: Check if item exists, return 404 if not found
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    # TODO: Get stored item and convert to Pydantic model
    stored_item = Item.model_validate(items[item_id])
    # TODO: Get only the fields that were set using item.dict(exclude_unset=True)
    update_data = item.model_dump(exclude_unset=True)
    # TODO: Create updated model using stored_item_model.copy(update=update_data)
    updated_item = stored_item.copy(update=update_data)
    # TODO: Store updated item using jsonable_encoder and return the model
    items[item_id] = updated_item.model_dump()
    return items[item_id]