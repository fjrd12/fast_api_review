"""
Response Status Code - HTTP Status Code Management

This module demonstrates how to specify and control HTTP status codes in FastAPI responses.
Understanding and properly using HTTP status codes is crucial for building RESTful APIs
that communicate effectively with clients about the result of their requests.

Key concepts covered:
- Setting custom status codes using the status_code parameter
- Using FastAPI's status module for semantic status codes
- Understanding when to use different HTTP status codes
- RESTful API conventions for status codes
- Client communication through status codes

HTTP Status Code Categories:
- 1xx: Informational responses
- 2xx: Success responses (200 OK, 201 Created, 204 No Content)
- 3xx: Redirection responses
- 4xx: Client error responses (400 Bad Request, 404 Not Found)
- 5xx: Server error responses (500 Internal Server Error)

Common REST API Status Codes:
- 200 OK: Standard successful response
- 201 Created: Resource successfully created
- 204 No Content: Successful request with no content to return
- 400 Bad Request: Invalid request format or parameters
- 401 Unauthorized: Authentication required
- 403 Forbidden: Access denied
- 404 Not Found: Resource not found
- 422 Unprocessable Entity: Validation error
- 500 Internal Server Error: Server-side error

Best Practices:
- Use 201 for successful resource creation (POST endpoints)
- Use 200 for successful retrieval or updates
- Use 204 for successful deletion
- Be consistent across your API
- Use semantic constants from fastapi.status module
"""

from fastapi import FastAPI
from fastapi import status

app = FastAPI()

# Create a POST endpoint at "/items/" that:
# 1. Accepts a "name" parameter as a query parameter (string)
# 2. Returns a dictionary with the name
# 3. Uses status code 201 (Created) instead of the default 200
# Hint: Use the status_code parameter in the decorator
# Example: @app.post("/items/", status_code=???)
# For query parameters, just define: def create_item(name: str):
# Hint: from fastapi import status
# Then use: status.HTTP_201_CREATED

@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    """
    Create a new item with custom HTTP status code.
    
    This endpoint demonstrates how to use custom HTTP status codes in FastAPI.
    Instead of returning the default 200 OK, it returns 201 Created, which is
    the appropriate status code for successful resource creation.
    
    The endpoint accepts a name as a query parameter and returns a simple
    dictionary containing the provided name. This simulates creating a new
    item resource.
    
    Args:
        name (str): The name of the item to create (provided as query parameter)
    
    Returns:
        dict: A dictionary containing the item name
        
    HTTP Status Code:
        201 Created: Indicates that the request has succeeded and a new resource
        has been created as a result. This is the standard response for successful
        POST requests that create new resources.
    
    Query Parameters:
        - name (str, required): The name for the new item
    
    Example Request:
        POST /items/?name=laptop
        
    Example Response:
        HTTP/1.1 201 Created
        Content-Type: application/json
        
        {
            "name": "laptop"
        }
    
    RESTful Design:
        This endpoint follows RESTful conventions by:
        - Using POST method for resource creation
        - Returning 201 Created status code for successful creation
        - Returning the created resource data in the response body
    
    Status Code Best Practice:
        Using status.HTTP_201_CREATED instead of hardcoding 201 provides:
        - Better code readability and self-documentation
        - IDE autocompletion support
        - Consistency with FastAPI conventions
        - Protection against typos in status codes
    
    Alternative Status Codes for Similar Operations:
        - 200 OK: For updates to existing resources (PUT/PATCH)
        - 204 No Content: For successful deletion (DELETE)
        - 202 Accepted: For asynchronous processing
        - 400 Bad Request: For invalid input data
        - 409 Conflict: If resource already exists
    
    Note:
        In a real application, this would typically:
        - Validate the input data more thoroughly
        - Save the item to a database
        - Return the complete created resource with an ID
        - Handle potential errors (duplicate names, validation failures)
    """
    return {"name": name}


