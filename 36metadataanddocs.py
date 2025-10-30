from fastapi import FastAPI

# TODO: Create a description for your API using Markdown
# Include sections for Items and Users
# Example format:
# """
# Task Management API description here. 🚀
#
# ## Items
# Description of items functionality
#
# ## Users
# Description of users functionality
# """
description = """\
# Task Management API

## Items
This API allows you to manage tasks and items efficiently.

## Users
This API provides user management functionalities.
"""

# TODO: Define metadata for tags
# Create a list with two dictionaries for 'users' and 'items' tags
# Each should have: name, description, and optionally externalDocs
tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users"
    },
    {
        "name": "items",
        "description": "Operations with items"
    }
]

# TODO: Create FastAPI application with metadata
# Include: title, description, summary, version, terms_of_service,
# contact (name, url, email), license_info (name, url),
# and openapi_tags
app = FastAPI(
    title="Task Management API",
    description=description,
    version="1.0.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "API Support",
        "url": "http://example.com/support",
        "email": "support@example.com"
    },
    license_info={
        "name": "MIT License",
        "url": "http://example.com/license"
    },
    openapi_tags=tags_metadata
)


@app.get("/")
async def root():
    """Root endpoint to verify the API is running."""
    # TODO: Return a welcome message
    # Return: {"message": "Welcome to Task Management API"}
    return {"message": "Welcome to Task Management API"}


# Add tags=["items"] to this endpoint
@app.get("/items/", tags=["items"])
async def read_items():
    """Get all available items."""
    # Return a list of items
    # Return: [{"id": 1, "name": "Task Manager"}, {"id": 2, "name": "Code Editor"}]
    return [{"id": 1, "name": "Task Manager"}, {"id": 2, "name": "Code Editor"}]


# TODO: Add tags=["users"] to this endpoint
@app.get("/users/", tags=["users"])
async def read_users():
    """Get all users."""
    # TODO: Return a list of users
    return [{"username": "johndoe"}, {"username": "janedoe"}]

