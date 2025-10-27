# Path Parameters and Numeric Validations - Following Official FastAPI Tutorial
# Learn how to add validation constraints to path parameters

from fastapi import FastAPI
from fastapi import Path, Query
from typing import List, Dict
# Import Path and Query from fastapi for advanced parameter validation

# Create FastAPI application instance
app = FastAPI()

# Sample database for demonstration purposes
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# Order matters: The path is evaluated first, then query parameters
# Path parameters are required and come from the URL path
# Query parameters are optional and come after the '?' in the URL

# Step 1: Add validation to path parameters
# This endpoint demonstrates basic path parameter validation using Path()
# Path(ge=1) adds a constraint that item_id must be >= 1
@app.get("/items/{item_id}")
async def get_item(item_id: int = Path(ge=1)):
    """
    Get an item by ID with path parameter validation.
    
    - item_id: Must be an integer >= 1
    - Returns the item_id in the response
    - Will return 422 error if item_id < 1
    """
    return {"item_id": item_id}

# Step 2: Combine Path and Query validations
# This endpoint shows how to use both Path and Query validations together
# Multiple constraints can be applied to the same parameter
@app.get("/items/{item_id}/details")
async def get_item_details(item_id: int = Path(ge=1, le=1000, description="The ID of the item"),
                           q: str | None = Query(default=None, max_length=50)):
    """
    Get detailed item information with both path and query validation.
    
    Path parameter:
    - item_id: Must be integer between 1 and 1000 (inclusive)
    - Includes description for API documentation
    
    Query parameter:
    - q: Optional string with max length of 50 characters
    - Can be omitted from the request
    """
    return {"item_id": item_id, "q": q, "details": "Item details here"}

# Step 3: Add metadata to path parameters
# This endpoint demonstrates adding documentation metadata to path parameters
# title and description help generate better API documentation
@app.get("/users/{user_id}")
async def get_user(user_id: int = Path(title="User ID", description="The ID of the user to get", ge=1)):
    """
    Get user profile with documented path parameter.
    
    Path parameter:
    - user_id: Integer >= 1
    - Has title "User ID" for documentation
    - Has description explaining the parameter's purpose
    - These metadata fields appear in the auto-generated API docs
    """
    return {"user_id": user_id, "message": f"User {user_id} profile"}