"""
FastAPI Sub-Dependencies Tutorial

This module demonstrates advanced dependency injection patterns using sub-dependencies
in FastAPI. Sub-dependencies allow you to create hierarchical dependency chains where
one dependency depends on another, enabling sophisticated parameter processing and
data flow patterns throughout your application.

Key Concepts:
- Sub-dependency patterns for hierarchical data processing
- Dependency chaining and composition techniques
- Cookie fallback mechanisms for enhanced user experience
- Parameter extraction and transformation pipelines

Learning Objectives:
- Master sub-dependency creation and chaining patterns
- Understand dependency resolution order and execution flow
- Implement fallback mechanisms using cookies and query parameters
- Build reusable dependency hierarchies for complex applications

Use Cases:
- User preference systems with query/cookie fallbacks
- Authentication chains with multiple verification steps
- Data transformation pipelines through dependency layers
- Complex parameter validation and processing workflows

Architecture Benefits:
- Modular dependency design for better code organization
- Reusable components that can be combined flexibly
- Clear separation of concerns in parameter processing
- Enhanced testability through isolated dependency units

Author: FastAPI Tutorial Series
Version: 1.0
Python: 3.11+
FastAPI: 0.104+
"""

from typing import Annotated

from fastapi import Cookie, Depends, FastAPI

app = FastAPI()


# Create the first dependency (query_extractor)
# This should extract an optional query parameter 'q' and return it
def query_extractor(q: str | None = None):
    """
    Base dependency function for extracting query parameters from HTTP requests.
    
    This function serves as the foundation of the sub-dependency chain, handling
    the initial extraction of search query parameters from incoming HTTP requests.
    It demonstrates the basic building block of FastAPI's dependency injection
    system and serves as a sub-dependency for more complex parameter processing.
    
    This dependency represents the first level in a hierarchical dependency chain,
    providing a clean interface for query parameter extraction that can be reused
    across multiple endpoints and composed with other dependencies.
    
    Args:
        q (str | None, optional): Search query parameter extracted from the URL.
            Can be None if no query parameter is provided in the request.
            Defaults to None.
    
    Returns:
        str | None: The extracted query parameter value, or None if not provided.
            This return value is passed to any dependencies that depend on this one.
    
    Example Usage:
        ```python
        # Direct usage (rarely used directly)
        result = query_extractor(q="search_term")
        print(result)  # "search_term"
        
        # As a sub-dependency (common pattern)
        @app.get("/search/")
        async def search(query: str = Depends(query_extractor)):
            return {"query": query}
        ```
    
    HTTP Request Examples:
        ```bash
        # Request with query parameter
        GET /items/?q=laptop
        # query_extractor receives: q="laptop"
        # Returns: "laptop"
        
        # Request without query parameter
        GET /items/
        # query_extractor receives: q=None
        # Returns: None
        
        # Request with empty query parameter
        GET /items/?q=
        # query_extractor receives: q=""
        # Returns: ""
        ```
    
    Dependency Chain Position:
        - **Level 1 (Base)**: Extracts raw query parameter
        - **Used by**: query_or_cookie_extractor (Level 2)
        - **Dependencies**: None (base dependency)
    
    Design Patterns:
        - **Single Responsibility**: Only handles query parameter extraction
        - **Composability**: Can be used as building block for complex dependencies
        - **Reusability**: Can be used across multiple endpoints
        - **Testability**: Simple function with clear input/output
    
    Sub-Dependency Benefits:
        - **Modularity**: Separated concerns for better code organization
        - **Reusability**: Base functionality can be shared across dependencies
        - **Testing**: Easier to test individual components
        - **Flexibility**: Can be combined with other dependencies in various ways
    
    Performance Notes:
        - Minimal overhead as a simple parameter extraction
        - FastAPI caches dependency results within request scope
        - No expensive operations or external calls
        - Direct parameter passthrough for optimal performance
    
    Production Considerations:
        - Consider input validation for query parameters
        - Add logging for monitoring search patterns
        - Implement query sanitization for security
        - Consider query length limits to prevent abuse
    """
    return q


# Create the second dependency (query_or_cookie_extractor) 
# This should depend on query_extractor and also check for a last_query cookie
# Parameters: q: Annotated[str, Depends(query_extractor)], last_query: Annotated[str | None, Cookie()] = None
def query_or_cookie_extractor(
    q: Annotated[str, Depends(query_extractor)],
    last_query: Annotated[str | None, Cookie()] = None,
):
    """
    Advanced dependency that combines query parameters with cookie fallback mechanism.
    
    This function demonstrates sophisticated sub-dependency patterns by depending on
    the query_extractor function while also implementing a cookie-based fallback system.
    It showcases how FastAPI can compose multiple dependency sources to create intelligent
    parameter resolution with user experience enhancements.
    
    The dependency implements a priority system where URL query parameters take precedence
    over stored cookie values, providing a seamless user experience where previous searches
    can be automatically restored when no new query is provided.
    
    Sub-Dependency Architecture:
        1. **Primary Source**: Depends on query_extractor for URL parameters
        2. **Fallback Source**: Reads last_query cookie for user preference persistence
        3. **Resolution Logic**: Prioritizes active queries over stored preferences
    
    Args:
        q (Annotated[str, Depends(query_extractor)]): Query parameter extracted through
            the query_extractor sub-dependency. This creates a dependency chain where
            FastAPI first calls query_extractor, then passes the result to this function.
        last_query (Annotated[str | None, Cookie()], optional): Cookie value containing
            the user's last search query for persistence across sessions. Defaults to None.
    
    Returns:
        str | None: The resolved query value based on priority logic:
            - Returns `q` if a query parameter is provided (priority source)
            - Returns `last_query` if no query parameter but cookie exists (fallback)
            - Returns None if neither source provides a value
    
    Resolution Logic Flow:
        ```python
        if q:              # Query parameter provided
            return q       # Use current query (highest priority)
        else:              # No query parameter
            return last_query  # Use cookie fallback (lower priority)
        ```
    
    Example Scenarios:
        ```python
        # Scenario 1: New search query provided
        # Request: GET /items/?q=laptops
        # Cookie: last_query="phones"
        # Result: "laptops" (query takes priority)
        
        # Scenario 2: No query, but cookie exists
        # Request: GET /items/
        # Cookie: last_query="phones" 
        # Result: "phones" (cookie fallback)
        
        # Scenario 3: No query, no cookie
        # Request: GET /items/
        # Cookie: (not set)
        # Result: None (no source available)
        
        # Scenario 4: Empty query string
        # Request: GET /items/?q=
        # Cookie: last_query="phones"
        # Result: "phones" (empty string is falsy, uses cookie)
        ```
    
    HTTP Request Examples:
        ```bash
        # Priority: Query parameter over cookie
        curl -H "Cookie: last_query=old_search" \
             "http://localhost:8000/items/?q=new_search"
        # Returns: {"q_or_cookie": "new_search"}
        
        # Fallback: Cookie when no query
        curl -H "Cookie: last_query=saved_search" \
             "http://localhost:8000/items/"
        # Returns: {"q_or_cookie": "saved_search"}
        
        # No sources: Both missing
        curl "http://localhost:8000/items/"
        # Returns: {"q_or_cookie": null}
        ```
    
    Dependency Chain Visualization:
        ```
        HTTP Request
            │
            ├─ Query Parameter 'q' ──► query_extractor() ──┐
            │                                              │
            └─ Cookie 'last_query' ─────────────────────► query_or_cookie_extractor()
                                                           │
                                                           ▼
                                                    Final Result
        ```
    
    Sub-Dependency Benefits:
        - **Separation of Concerns**: query_extractor handles only query extraction
        - **Reusability**: query_extractor can be used independently elsewhere
        - **Composability**: Easy to add more dependency layers
        - **Testability**: Each dependency can be tested in isolation
        - **Flexibility**: Can modify fallback logic without affecting query extraction
    
    User Experience Enhancements:
        - **Persistence**: Users' searches are remembered across sessions
        - **Convenience**: No need to re-type previous searches
        - **Progressive Enhancement**: Works with and without cookies
        - **Intuitive Behavior**: Current query always takes precedence
    
    Advanced Patterns:
        ```python
        # Multiple fallback sources
        def multi_source_extractor(
            q: str = Depends(query_extractor),
            cookie_query: str | None = Cookie(None),
            header_query: str | None = Header(None)
        ):
            return q or cookie_query or header_query or "default"
        
        # Conditional dependency chains
        def smart_extractor(
            q: str = Depends(query_extractor),
            user: dict = Depends(get_current_user)
        ):
            if user.get("preferences", {}).get("save_searches"):
                # Use cookie fallback for users who opted in
                return Depends(query_or_cookie_extractor)
            else:
                # Direct query only for privacy-conscious users
                return q
        ```
    
    Security Considerations:
        - **Cookie Validation**: Validate cookie contents to prevent injection
        - **Size Limits**: Limit cookie size to prevent abuse
        - **Sanitization**: Clean both query and cookie values
        - **Privacy**: Consider user consent for search history storage
    
    Performance Notes:
        - **Dependency Caching**: FastAPI caches results within request scope
        - **Minimal Overhead**: Simple string comparison and fallback logic
        - **Cookie Reading**: Automatic HTTP header parsing by FastAPI
        - **Memory Efficient**: No complex processing or storage requirements
    
    Production Enhancements:
        - **Validation**: Add input validation for both sources
        - **Logging**: Track usage patterns for analytics
        - **Encryption**: Consider encrypting sensitive search terms in cookies
        - **Expiration**: Implement cookie expiration for privacy
        - **Compression**: Use cookie compression for large search terms
    
    Testing Strategies:
        ```python
        # Test sub-dependency isolation
        def test_query_extractor():
            result = query_extractor(q="test")
            assert result == "test"
        
        # Test fallback logic
        def test_cookie_fallback():
            result = query_or_cookie_extractor(q=None, last_query="cookie_value")
            assert result == "cookie_value"
        
        # Test priority logic
        def test_query_priority():
            result = query_or_cookie_extractor(q="query_value", last_query="cookie_value")
            assert result == "query_value"
        ```
    """
    # TODO: If not q, return last_query, otherwise return q
    if not q:
        return last_query
    return q


# Create a GET /items/ path operation 
# Use query_or_cookie_extractor as dependency
# Parameter: query_or_default: Annotated[str, Depends(query_or_cookie_extractor)]
# Return: {"q_or_cookie": query_or_default}
@app.get("/items/")
async def read_query(
    query_or_default: Annotated[str, Depends(query_or_cookie_extractor)],
):
    """
    Retrieve items using sophisticated sub-dependency chain for query resolution.
    
    This endpoint demonstrates the practical application of sub-dependencies in FastAPI,
    showcasing how complex parameter resolution can be achieved through dependency
    composition. The endpoint automatically resolves search queries from multiple sources
    with intelligent fallback mechanisms, providing an enhanced user experience.
    
    The endpoint leverages a two-level dependency chain:
    1. **Level 1**: query_extractor extracts URL query parameters
    2. **Level 2**: query_or_cookie_extractor adds cookie fallback logic
    3. **Level 3**: This endpoint receives the final resolved value
    
    Dependency Chain Flow:
        ```
        HTTP Request
            │
            ├─ URL: ?q=search ──► query_extractor ──┐
            │                                       │
            └─ Cookie: last_query ─────────────────► query_or_cookie_extractor ──► read_query
                                                     │
                                                     ▼
                                              Resolved Query Value
        ```
    
    Args:
        query_or_default (Annotated[str, Depends(query_or_cookie_extractor)]): 
            The resolved query value from the sub-dependency chain. This parameter
            automatically receives the result of the query_or_cookie_extractor 
            dependency, which itself depends on query_extractor.
            
            Possible values:
            - String: Active query parameter or cookie fallback value
            - None: No query source available from either parameter or cookie
    
    Returns:
        dict: Response dictionary containing the resolved query information:
            ```json
            {
                "q_or_cookie": "resolved_query_value_or_null"
            }
            ```
    
    HTTP Status Codes:
        - **200 OK**: Successfully processed request with or without query
        - **422 Unprocessable Entity**: Invalid cookie or parameter format (rare)
    
    Example Requests and Responses:
        ```bash
        # Case 1: New search query (highest priority)
        curl -H "Cookie: last_query=old_search" \
             "http://localhost:8000/items/?q=new_search"
        
        Response:
        {
            "q_or_cookie": "new_search"
        }
        
        # Case 2: Cookie fallback (no URL query)
        curl -H "Cookie: last_query=remembered_search" \
             "http://localhost:8000/items/"
        
        Response:
        {
            "q_or_cookie": "remembered_search"
        }
        
        # Case 3: No sources available
        curl "http://localhost:8000/items/"
        
        Response:
        {
            "q_or_cookie": null
        }
        
        # Case 4: Empty query uses cookie fallback
        curl -H "Cookie: last_query=fallback_search" \
             "http://localhost:8000/items/?q="
        
        Response:
        {
            "q_or_cookie": "fallback_search"
        }
        ```
    
    Dependency Resolution Process:
        1. **FastAPI receives HTTP request** with potential query and cookie data
        2. **query_extractor dependency** extracts 'q' parameter from URL
        3. **query_or_cookie_extractor dependency** receives query result and cookie
        4. **Resolution logic** determines final value based on priority rules
        5. **read_query endpoint** receives resolved value and formats response
        6. **JSON response** returned to client with resolved query information
    
    Real-World Applications:
        ```python
        # Search with pagination and filtering
        @app.get("/products/")
        async def search_products(
            query: str = Depends(query_or_cookie_extractor),
            skip: int = 0,
            limit: int = 20,
            category: str | None = None
        ):
            # Use resolved query for database search
            filters = {"category": category} if category else {}
            if query:
                filters["search"] = query
            
            products = database.search_products(
                filters=filters,
                offset=skip,
                limit=limit
            )
            
            return {
                "query": query,
                "products": products,
                "pagination": {"skip": skip, "limit": limit}
            }
        
        # User preference tracking
        @app.get("/recommendations/")
        async def get_recommendations(
            query: str = Depends(query_or_cookie_extractor),
            user: dict = Depends(get_current_user)
        ):
            # Use query for personalized recommendations
            if query:
                # Update user search history
                await update_search_history(user["id"], query)
                
                # Get query-based recommendations
                recommendations = await get_query_recommendations(query)
            else:
                # Get general recommendations
                recommendations = await get_user_recommendations(user["id"])
            
            return {
                "query": query,
                "recommendations": recommendations,
                "personalized": bool(query)
            }
        ```
    
    Frontend Integration:
        ```javascript
        // JavaScript client example
        class SearchClient {
            async search(query = null) {
                const url = query 
                    ? `/items/?q=${encodeURIComponent(query)}`
                    : '/items/';  // Will use cookie fallback
                
                const response = await fetch(url, {
                    credentials: 'include'  // Include cookies
                });
                
                const data = await response.json();
                
                // Update UI with resolved query
                this.updateSearchUI(data.q_or_cookie);
                
                return data;
            }
            
            // Save search to cookie for persistence
            saveLastSearch(query) {
                document.cookie = `last_query=${encodeURIComponent(query)}; path=/; max-age=604800`;
            }
        }
        ```
    
    Testing Scenarios:
        ```python
        # Example test cases for the endpoint
        from fastapi.testclient import TestClient
        
        def test_query_parameter_priority():
            # Test that query parameter takes priority over cookie
            client = TestClient(app)
            response = client.get(
                "/items/?q=new_search",
                cookies={"last_query": "old_search"}
            )
            assert response.status_code == 200
            assert response.json() == {"q_or_cookie": "new_search"}
        
        def test_cookie_fallback():
            # Test that cookie is used when no query parameter
            client = TestClient(app)
            response = client.get(
                "/items/",
                cookies={"last_query": "cookie_search"}
            )
            assert response.status_code == 200
            assert response.json() == {"q_or_cookie": "cookie_search"}
        
        def test_no_sources():
            # Test behavior when neither query nor cookie available
            client = TestClient(app)
            response = client.get("/items/")
            assert response.status_code == 200
            assert response.json() == {"q_or_cookie": None}
        
        def test_empty_query_uses_cookie():
            # Test that empty query parameter uses cookie fallback
            client = TestClient(app)
            response = client.get(
                "/items/?q=",
                cookies={"last_query": "fallback_search"}
            )
            assert response.status_code == 200
            assert response.json() == {"q_or_cookie": "fallback_search"}
        ```
    
    Performance Characteristics:
        - **Dependency Caching**: Sub-dependencies are cached within request scope
        - **Minimal Overhead**: Simple parameter extraction and logic
        - **No External Calls**: Pure parameter processing without I/O
        - **Linear Complexity**: O(1) time complexity for resolution
    
    Security Best Practices:
        - **Input Validation**: Validate both query and cookie contents
        - **XSS Prevention**: Escape output if used in HTML contexts
        - **Size Limits**: Limit query and cookie sizes
        - **Rate Limiting**: Implement request rate limiting
        - **Logging**: Log search patterns for security monitoring
    
    Production Enhancements:
        - **Caching**: Implement response caching for popular queries
        - **Analytics**: Track query resolution patterns
        - **Personalization**: Integrate with user preference systems
        - **A/B Testing**: Test different fallback strategies
        - **Monitoring**: Monitor dependency chain performance
        - **Documentation**: Auto-generate API docs showing dependency flow
    
    Extension Patterns:
        ```python
        # Multiple fallback levels
        @app.get("/advanced-search/")
        async def advanced_search(
            query: str = Depends(query_or_cookie_extractor),
            user_prefs: dict = Depends(get_user_preferences),
            trending: list = Depends(get_trending_searches)
        ):
            final_query = query or user_prefs.get("default_search") or trending[0]
            return {"query": final_query, "source": determine_source(query, user_prefs)}
        
        # Conditional sub-dependencies
        async def smart_query_extractor(
            user: dict = Depends(get_current_user)
        ):
            if user.get("preferences", {}).get("remember_searches"):
                return Depends(query_or_cookie_extractor)
            else:
                return Depends(query_extractor)  # No cookie fallback for privacy users
        ```
    
    This endpoint demonstrates the power of FastAPI's sub-dependency system for creating
    sophisticated parameter resolution with excellent user experience and clean code architecture!
    """
    # Return dict with q_or_cookie key
    return {"q_or_cookie": query_or_default}