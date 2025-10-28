"""
19jsoncompatibleencoder.py

JSON Compatible Encoder in FastAPI
==================================

This module demonstrates the use of FastAPI's jsonable_encoder utility for converting
complex Python objects (like Pydantic models, datetime objects, etc.) into JSON-compatible
formats that can be safely serialized and stored or transmitted.

Key Concepts Covered:
- JSON-compatible data conversion using jsonable_encoder
- Handling complex data types (datetime, Pydantic models)
- Database storage simulation with encoded data
- Type-safe data serialization patterns
- Integration between Pydantic models and JSON storage

The jsonable_encoder is essential when working with databases or external systems
that require pure JSON-compatible data structures rather than Python objects.

Dependencies:
- fastapi: Web framework and jsonable_encoder utility
- pydantic: Data validation and model definition
- datetime: Date and time handling
- typing: Type hints for better code clarity

Learning Objectives:
- Understand when and why to use jsonable_encoder
- Learn to handle complex data types in API responses
- Practice data serialization for storage systems
- Implement type-safe data conversion patterns
- Handle datetime objects in JSON responses

Production Considerations:
- Always encode complex objects before database storage
- Consider timezone handling for datetime objects
- Implement proper error handling for encoding failures
- Use consistent encoding patterns across the application
- Consider performance implications of repeated encoding

Author: FastAPI Tutorial Series
Date: October 2025
Version: 1.0
"""

from datetime import datetime
from typing import Union

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

fake_db = {}


class Item(BaseModel):
    """
    Item model with complex data types for JSON encoding demonstration.
    
    This Pydantic model includes a datetime field to demonstrate how
    jsonable_encoder handles complex data types that are not natively
    JSON-serializable.
    
    Attributes:
        title (str): The title/name of the item
        timestamp (datetime): When the item was created or last modified
        description (str | None): Optional detailed description of the item
        
    Example:
        ```python
        item = Item(
            title="Sample Item",
            timestamp=datetime.now(),
            description="This is a sample item for testing"
        )
        ```
        
    JSON Encoding Challenge:
        The datetime field cannot be directly serialized to JSON without
        conversion. This is where jsonable_encoder becomes essential.
        
    Encoded Output:
        ```json
        {
            "title": "Sample Item",
            "timestamp": "2025-10-28T10:30:00.123456",
            "description": "This is a sample item for testing"
        }
        ```
        
    Note:
        The datetime object is automatically converted to ISO format string
        when using jsonable_encoder, making it JSON-compatible.
    """
    title: str
    timestamp: datetime
    description: Union[str, None] = None


app = FastAPI()


@app.put("/items/{id}")
def update_item(id: str, item: Item):
    """
    Update an item using JSON-compatible encoding for storage.
    
    This endpoint demonstrates the proper use of jsonable_encoder to convert
    a Pydantic model containing complex data types (like datetime) into a
    JSON-compatible format suitable for database storage or transmission.
    
    Args:
        id (str): The unique identifier for the item to update
        item (Item): The item data containing title, timestamp, and optional description
        
    Returns:
        dict: The JSON-compatible encoded item data that was stored
        
    Process:
        1. Receives a Pydantic Item model with datetime field
        2. Converts the model to JSON-compatible format using jsonable_encoder
        3. Stores the encoded data in the simulated database
        4. Returns the encoded data to confirm successful storage
        
    Example Request:
        PUT /items/123
        Content-Type: application/json
        
        {
            "title": "Updated Item",
            "timestamp": "2025-10-28T10:30:00.123456",
            "description": "This item has been updated"
        }
        
    Example Response:
        Status: 200 OK
        Content-Type: application/json
        
        {
            "title": "Updated Item",
            "timestamp": "2025-10-28T10:30:00.123456",
            "description": "This item has been updated"
        }
        
    JSON Encoding Benefits:
        - Converts datetime objects to ISO format strings
        - Handles Pydantic model serialization automatically
        - Ensures data is compatible with JSON storage systems
        - Maintains data type integrity during conversion
        - Provides consistent encoding across the application
        
    Database Storage:
        The encoded data is stored in fake_db[id] as a plain dictionary
        with all complex types converted to JSON-compatible formats.
        
    Note:
        In production, you would replace fake_db with a real database
        system that requires JSON-compatible data formats.
    """
    # TODO: Use jsonable_encoder to convert the Pydantic model to JSON-compatible format
    # TODO: Store the encoded item data in fake_db with the id as key
    # TODO: Return the encoded data to show it's working
    # Hint: json_compatible_item_data = jsonable_encoder(item)
    # Hint: fake_db[id] = json_compatible_item_data
    # Hint: return json_compatible_item_data
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data
    return json_compatible_item_data