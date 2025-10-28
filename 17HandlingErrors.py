"""
17HandlingErrors.py

Error Handling in FastAPI
========================

This module demonstrates comprehensive error handling patterns in FastAPI applications,
including HTTP exceptions, custom exceptions, and exception handlers.

Key Concepts Covered:
- HTTPException for standard HTTP errors
- Custom headers in error responses
- Custom exception classes
- Exception handlers for application-specific errors
- Error response formatting and status codes

Error handling is crucial for building robust APIs that provide meaningful feedback
to clients when operations fail or encounter unexpected conditions.

Dependencies:
- fastapi: Web framework for building APIs
- fastapi.responses: Response classes for custom error formatting

Learning Objectives:
- Understand when and how to raise HTTP exceptions
- Learn to add custom headers to error responses
- Create custom exception classes for domain-specific errors
- Implement exception handlers for consistent error formatting
- Apply proper HTTP status codes for different error scenarios

Production Considerations:
- Always provide meaningful error messages to help client debugging
- Use appropriate HTTP status codes following REST conventions
- Consider security implications of error messages (avoid exposing internal details)
- Implement consistent error response formats across the API
- Log errors appropriately for monitoring and debugging

Author: FastAPI Tutorial Series
Date: October 2025
Version: 1.0
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# Sample data (following official docs naming)
items = {"foo": "The Foo Wrestlers"}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    """
    Retrieve an item by ID with basic error handling.
    
    This endpoint demonstrates basic HTTP exception handling in FastAPI.
    It retrieves an item from the sample data store and raises a 404 error
    if the item is not found.
    
    Args:
        item_id (str): The unique identifier of the item to retrieve
        
    Returns:
        dict: A dictionary containing the item data if found
        
    Raises:
        HTTPException: 404 error if the item_id is not found in the items store
        
    Example Request:
        GET /items/foo
        
    Example Response (Success):
        {
            "item": "The Foo Wrestlers"
        }
        
    Example Response (Error):
        {
            "detail": "Item not found"
        }
        Status Code: 404
        
    Error Handling:
        - Returns 404 Not Found when item_id doesn't exist
        - Uses HTTPException for standard HTTP error responses
        - Provides meaningful error message in the detail field
        
    Note:
        This endpoint demonstrates the most basic form of error handling
        in FastAPI using HTTPException with a status code and detail message.
    """
    # Check if item_id exists in items
    # If not found, raise HTTPException with status_code=404, detail="Item not found"
    # If found, return {"item": items[item_id]}
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}


@app.get("/items-header/{item_id}")
async def read_item_header(item_id: str):
    """
    Retrieve an item by ID with custom headers in error responses.
    
    This endpoint demonstrates how to include custom headers in HTTP exception
    responses. It's useful for providing additional metadata or debugging
    information in error responses.
    
    Args:
        item_id (str): The unique identifier of the item to retrieve
        
    Returns:
        dict: A dictionary containing the item data if found
        
    Raises:
        HTTPException: 404 error with custom headers if the item_id is not found
        
    Example Request:
        GET /items-header/foo
        
    Example Response (Success):
        {
            "item": "The Foo Wrestlers"
        }
        Status Code: 200
        
    Example Response (Error):
        {
            "detail": "Item not found"
        }
        Status Code: 404
        Headers: X-Error: "There goes my error"
        
    Error Handling:
        - Returns 404 Not Found when item_id doesn't exist
        - Includes custom header "X-Error" with additional error context
        - Demonstrates how to pass headers parameter to HTTPException
        
    Use Cases:
        - Adding correlation IDs for error tracking
        - Providing additional error context for debugging
        - Including rate limiting information
        - Adding custom authentication challenges
        
    Note:
        Custom headers in error responses can be useful for client-side
        error handling and debugging, but should not expose sensitive information.
    """
    # Check if item_id exists in items
    # If not found, raise HTTPException with:
    #   - status_code=404
    #   - detail="Item not found" 
    #   - headers={"X-Error": "There goes my error"}
    # If found, return {"item": items[item_id]}
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found",headers={"X-Error": "There goes my error"})
    return {"item": items[item_id]}

# Create a custom exception class called UnicornException
# It should accept a name parameter in __init__
class UnicornException(Exception):
    """
    Custom exception for unicorn-related errors.
    
    This class demonstrates how to create custom exception classes in FastAPI
    applications for domain-specific error handling. Custom exceptions allow
    for more granular error handling and can carry additional context.
    
    Attributes:
        name (str): The name of the unicorn that caused the exception
        
    Example Usage:
        raise UnicornException(name="rainbow_unicorn")
        
    Benefits of Custom Exceptions:
        - Domain-specific error types for better code organization
        - Ability to carry custom data/context with the exception
        - Enables specific exception handlers for different error types
        - Improves code readability and maintainability
        
    Note:
        Custom exceptions should inherit from Python's base Exception class
        or a more specific exception type when appropriate.
    """
    def __init__(self, name: str):
        """
        Initialize the UnicornException with a unicorn name.
        
        Args:
            name (str): The name of the unicorn causing the exception
        """
        self.name = name
        super().__init__(f"Unicorn '{name}' caused an error")


#Add a custom exception handler for UnicornException
# Use @app.exception_handler(UnicornException)
# Return JSONResponse with status_code=418 and message about the unicorn
@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    """
    Custom exception handler for UnicornException.
    
    This function demonstrates how to create custom exception handlers in FastAPI
    that provide specific handling for custom exception types. Exception handlers
    allow you to customize the response format and behavior when specific
    exceptions are raised.
    
    Args:
        request (Request): The incoming request that triggered the exception
        exc (UnicornException): The custom exception instance that was raised
        
    Returns:
        JSONResponse: A custom JSON response with status code 418 and error details
        
    Response Format:
        {
            "message": "The 'unicorn_name' caused an error!"
        }
        Status Code: 418 (I'm a teapot)
        
    Exception Handler Benefits:
        - Consistent error response formatting across the application
        - Custom logic for different exception types
        - Access to both request context and exception details
        - Ability to log, transform, or enrich error responses
        
    Note:
        The 418 status code is used here for demonstration purposes.
        In production, use appropriate HTTP status codes (400-499 for client errors,
        500-599 for server errors).
    """
    return JSONResponse(
        status_code=418,
        content={"message": f"The'{exc.name}' caused an error!"},
    )


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    """
    Retrieve unicorn information with custom exception handling.
    
    This endpoint demonstrates how custom exceptions are used in FastAPI
    applications. It triggers a custom UnicornException for specific input
    values, showing how domain-specific errors can be handled differently
    from standard HTTP exceptions.
    
    Args:
        name (str): The name of the unicorn to retrieve
        
    Returns:
        dict: A dictionary containing the unicorn name if valid
        
    Raises:
        UnicornException: When the name is "yolo", demonstrating custom exception flow
        
    Example Request:
        GET /unicorns/sparkles
        
    Example Response (Success):
        {
            "unicorn_name": "sparkles"
        }
        Status Code: 200
        
    Example Request (Error):
        GET /unicorns/yolo
        
    Example Response (Error):
        {
            "message": "The 'yolo' caused an error!"
        }
        Status Code: 418
        
    Error Flow:
        1. Endpoint raises UnicornException for name "yolo"
        2. FastAPI catches the exception
        3. Custom exception handler processes the exception
        4. Handler returns formatted JSON response with status 418
        
    Learning Points:
        - Custom exceptions provide domain-specific error handling
        - Exception handlers enable consistent error response formatting
        - Different exception types can have different handling logic
        - Custom exceptions can carry context data (like the unicorn name)
        
    Note:
        This example uses "yolo" as a trigger value for demonstration.
        In real applications, custom exceptions would be raised based on
        actual business logic conditions.
    """
    # If name == "yolo", raise UnicornException(name=name)
    # Otherwise return {"unicorn_name": name}
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}