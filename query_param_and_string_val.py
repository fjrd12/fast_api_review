"""
FastAPI Query Parameters and String Validation Example

This module demonstrates advanced query parameter handling in FastAPI with
string validation, constraints, and search functionality using the Query class.

Key concepts covered:
- Query parameter validation with Query()
- String length constraints (min_length, max_length)
- Numeric constraints (ge, le) for integer parameters
- List comprehensions for data filtering
- Case-insensitive search functionality
- Parameter descriptions for API documentation

Run with: fastapi dev query_param_and_string_val.py
"""

from fastapi import FastAPI
from fastapi import Query
from typing import List, Dict

app = FastAPI(
    title="Query Parameters and String Validation Demo",
    description="A FastAPI application demonstrating advanced query parameter validation and search functionality",
    version="1.0.0"
)

# Sample database with items for demonstration
fake_items_db = [
    {"item_name": "Foo"}, 
    {"item_name": "Bar"}, 
    {"item_name": "Baz"}
]


@app.get("/items/")
async def read_items(q: str | None = Query(default=None, max_length=50)) -> List[Dict]:
    """
    Search items with optional query parameter validation.
    
    This endpoint demonstrates basic query parameter validation using the Query class.
    It performs a case-insensitive search through the items database and returns
    matching results.
    
    Args:
        q (str | None, optional): Search query string with maximum length of 50 characters.
                                 Defaults to None.
        
    Returns:
        List[Dict]: A list of items that match the search query. Returns empty list
                   if no query is provided or no matches are found.
        
    Query Parameter Validation:
        - max_length=50: Query string cannot exceed 50 characters
        - default=None: Parameter is optional
        
    Examples:
        GET /items/ -> []
        GET /items/?q=foo -> [{"item_name": "Foo"}]
        GET /items/?q=ba -> [{"item_name": "Bar"}, {"item_name": "Baz"}]
        GET /items/?q=xyz -> []
        
    Raises:
        422 Validation Error: If query string exceeds 50 characters
        
    Note:
        - Search is case-insensitive
        - Performs partial matching (substring search)
        - Returns empty array if no query parameter is provided
    """
    # List comprehension that looks for string q in the item_name field
    results = [item for item in fake_items_db if q and q.lower() in item["item_name"].lower()]
    return results


@app.get("/items/search/")
async def search_items(
    q: str = Query(min_length=3, max_length=50, description="Search query"),
    limit: int = Query(10, ge=1, le=100, description="Number of results of items")
) -> List[Dict]:
    """
    Advanced search with required query and result limiting.
    
    This endpoint demonstrates comprehensive query parameter validation including
    required parameters, string constraints, numeric constraints, and result pagination.
    It provides a more robust search functionality with input validation.
    
    Args:
        q (str): Required search query string. Must be between 3-50 characters.
        limit (int): Maximum number of results to return. Must be between 1-100.
                    Defaults to 10.
        
    Returns:
        List[Dict]: A list of items matching the search query, limited to the
                   specified number of results.
        
    Query Parameter Validation:
        q parameter:
            - min_length=3: Query must be at least 3 characters
            - max_length=50: Query cannot exceed 50 characters
            - Required: Parameter must be provided
            
        limit parameter:
            - ge=1: Must be greater than or equal to 1
            - le=100: Must be less than or equal to 100
            - default=10: Defaults to 10 if not specified
        
    Examples:
        GET /items/search/?q=foo -> [{"item_name": "Foo"}]
        GET /items/search/?q=bar&limit=1 -> [{"item_name": "Bar"}]
        GET /items/search/?q=ba&limit=1 -> [{"item_name": "Bar"}]
        
    Raises:
        422 Validation Error: If:
            - Query string is less than 3 characters or more than 50 characters
            - Limit is less than 1 or greater than 100
            - Query parameter is missing
            
    Note:
        - Search is case-insensitive and performs partial matching
        - Results are limited to the specified limit parameter
        - If no matches found, returns empty array
        - More strict validation than the basic /items/ endpoint
    """
    # List comprehension that looks for string q in the item_name field
    results = []
    results = [item for item in fake_items_db if q and q.lower() in item["item_name"].lower()]
    if len(results) > 0:
        results = results[:limit]
    return results