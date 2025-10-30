"""
FastAPI Middleware Basics - Lesson 31

This module demonstrates the fundamentals of middleware in FastAPI applications.
Middleware functions as a layer that sits between incoming requests and outgoing
responses, allowing you to process requests before they reach your endpoints
and modify responses before they're sent back to clients.

Middleware Use Cases:
    - Request/response timing and performance monitoring
    - Authentication and authorization validation
    - Request logging and analytics collection
    - CORS (Cross-Origin Resource Sharing) handling
    - Rate limiting and request throttling
    - Custom header injection and response modification
    - Error handling and request preprocessing

Key Concepts Covered:
    - HTTP middleware implementation with @app.middleware("http")
    - Request processing pipeline and call_next() pattern
    - Response header modification and custom header injection
    - Timing measurements with time.perf_counter() for precision
    - Middleware execution order and request/response flow
    - Interaction between middleware and API endpoints

Technical Implementation:
    - Asynchronous middleware functions for non-blocking execution
    - Request object access for incoming request inspection
    - Response object modification for custom header addition
    - Precise timing measurements for performance monitoring
    - Integration with FastAPI's dependency injection system

Production Applications:
    - Performance monitoring and APM (Application Performance Monitoring)
    - Security headers injection (HSTS, CSP, X-Frame-Options)
    - Request correlation IDs for distributed tracing
    - Custom authentication schemes and token validation
    - API usage analytics and monitoring systems

Security Considerations:
    - Middleware executes for ALL requests (be careful with heavy operations)
    - Ensure proper error handling to prevent request hanging
    - Validate middleware order to prevent security bypasses
    - Consider performance impact of middleware processing
    - Implement proper logging without exposing sensitive data

Learning Objectives:
    - Understand middleware execution flow in FastAPI
    - Implement custom middleware for cross-cutting concerns
    - Learn timing and performance measurement techniques
    - Practice request/response manipulation patterns
    - Build foundation for advanced middleware implementations

Author: FastAPI Learning Series
Created: 2025-10-30
Dependencies: FastAPI, Pydantic, time (built-in)
"""

import time
from fastapi import FastAPI, Request
from pydantic import BaseModel

# FastAPI application instance with middleware capabilities
app = FastAPI(
    title="FastAPI Middleware Basics",
    description="Demonstration of middleware fundamentals in FastAPI",
    version="1.0.0"
)

# Data model for item creation and validation
class Item(BaseModel):
    """
    Pydantic model representing an item in the application.
    
    This model defines the structure and validation rules for items
    that can be created and stored in the application. It demonstrates
    how middleware interacts with different types of endpoints including
    those that process request bodies.
    
    Attributes:
        name (str): The unique identifier and display name for the item.
                   Required field that will be used as the dictionary key.
        description (str, optional): Additional details about the item.
                                   Defaults to None if not provided.
    
    Validation Features:
        - Automatic type conversion and validation via Pydantic
        - Required field validation for name attribute
        - Optional field handling with default values
        - JSON serialization/deserialization support
        - Integration with FastAPI's automatic request body parsing
    
    Usage Examples:
        ```python
        # Creating an item with description
        item = Item(name="laptop", description="High-performance laptop")
        
        # Creating an item without description
        item = Item(name="mouse")  # description will be None
        
        # JSON representation
        item_dict = item.model_dump()
        # Output: {"name": "laptop", "description": "High-performance laptop"}
        ```
    
    Middleware Integration:
        - Request processing time includes Pydantic validation
        - Middleware sees the raw request before model validation
        - Response timing includes model serialization time
        - Demonstrates middleware working with POST requests and request bodies
    
    Production Considerations:
        - Add field validators for business logic validation
        - Implement custom serialization for complex data types
        - Consider field aliases for API compatibility
        - Add documentation strings for automatic API documentation
        - Implement proper error handling for validation failures
    
    Related Endpoints:
        - POST /items/ - Creates new items using this model
        - GET /items/{item_id} - Retrieves items created with this model
    """
    name: str
    description: str = None


# In-memory data store for demonstration purposes
items = {
    "foo": {"name": "The Foo Wrestlers"},
    "bar": {"name": "The Bar Tenders"}
}
"""
Sample data store simulating a database for middleware demonstration.

This dictionary serves as a simple in-memory database to demonstrate
how middleware processes requests for different types of operations:
- Read operations (GET requests)
- Write operations (POST requests)
- Data retrieval and storage timing

Initial Data:
    - "foo": Sample item representing "The Foo Wrestlers"
    - "bar": Sample item representing "The Bar Tenders"

Middleware Interaction:
    - GET requests: Middleware measures data retrieval time
    - POST requests: Middleware measures data creation and validation time
    - All operations: Custom headers added regardless of data operation type

Production Note:
    In production applications, this would be replaced with:
    - Database connections (PostgreSQL, MySQL, MongoDB)
    - ORM operations (SQLAlchemy, Tortoise ORM)
    - Cache systems (Redis, Memcached)
    - External API calls and integrations
    
    Middleware timing would then measure:
    - Database query execution time
    - Network latency for external services
    - Cache hit/miss performance
    - Data serialization/deserialization overhead
"""


# Performance monitoring middleware implementation
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    HTTP middleware that measures and reports request processing time.
    
    This middleware demonstrates the fundamental pattern of FastAPI middleware
    by intercepting all HTTP requests, measuring their processing time, and
    adding custom headers to responses. It showcases the request/response
    lifecycle and how middleware can add cross-cutting functionality.
    
    Args:
        request (Request): The incoming HTTP request object containing
                          headers, body, path, method, and other request data
        call_next (Callable): Function that processes the request through
                              the rest of the application stack and returns response
    
    Returns:
        Response: The HTTP response with added X-Process-Time header
    
    Processing Flow:
        1. Record start time using high-precision timer
        2. Call next middleware/endpoint in the chain
        3. Calculate total processing time after response
        4. Add custom header with timing information
        5. Return modified response to client
    
    Timing Methodology:
        - Uses time.perf_counter() for precise timing measurements
        - Measures wall-clock time including I/O operations
        - Includes time for: request parsing, endpoint processing,
          response generation, and other middleware execution
        - Precision: Nanosecond accuracy on most systems
    
    Header Format:
        - Header Name: "X-Process-Time"
        - Header Value: String representation of seconds (e.g., "0.002341")
        - Client Usage: Can be parsed as float for performance monitoring
    
    Use Cases:
        - Performance monitoring and alerting
        - Identifying slow endpoints and bottlenecks
        - SLA compliance monitoring
        - Debugging performance issues
        - Load testing analysis and optimization
    
    Client Integration Examples:
        ```javascript
        // JavaScript: Monitor API performance
        fetch('/api/endpoint')
            .then(response => {
                const processTime = parseFloat(response.headers.get('X-Process-Time'));
                console.log(`Request took ${processTime * 1000}ms`);
                return response.json();
            });
        ```
        
        ```python
        # Python requests: Performance monitoring
        import requests
        response = requests.get('http://localhost:8000/items/foo')
        process_time = float(response.headers['X-Process-Time'])
        print(f"API call took {process_time:.3f} seconds")
        ```
    
    Production Enhancements:
        ```python
        @app.middleware("http")
        async def enhanced_timing_middleware(request: Request, call_next):
            # Add request correlation ID
            correlation_id = str(uuid.uuid4())
            request.state.correlation_id = correlation_id
            
            # Record detailed timing
            start_time = time.perf_counter()
            
            # Log request start
            logger.info(f"Request started: {request.method} {request.url}", 
                       extra={"correlation_id": correlation_id})
            
            try:
                response = await call_next(request)
                
                # Calculate timing
                process_time = time.perf_counter() - start_time
                
                # Add multiple headers
                response.headers["X-Process-Time"] = str(process_time)
                response.headers["X-Correlation-ID"] = correlation_id
                response.headers["X-Server-ID"] = os.getenv("SERVER_ID", "unknown")
                
                # Log successful completion
                logger.info(f"Request completed: {response.status_code}", 
                           extra={
                               "correlation_id": correlation_id,
                               "process_time": process_time,
                               "status_code": response.status_code
                           })
                
                return response
                
            except Exception as e:
                # Log errors with timing
                process_time = time.perf_counter() - start_time
                logger.error(f"Request failed: {str(e)}", 
                           extra={
                               "correlation_id": correlation_id,
                               "process_time": process_time,
                               "error": str(e)
                           })
                raise
        ```
    
    Monitoring Integration:
        - Export metrics to Prometheus/Grafana
        - Send timing data to APM systems (DataDog, New Relic)
        - Alert on slow requests exceeding thresholds
        - Track performance trends over time
    
    Performance Considerations:
        - Minimal overhead: perf_counter() is very fast
        - String conversion cost is negligible
        - No blocking operations in middleware
        - Header addition doesn't impact response body
        - Consider sampling for extremely high-traffic applications
    
    Security Notes:
        - Timing information may reveal system performance characteristics
        - Consider removing in production if timing data is sensitive
        - Monitor for timing attacks on authentication endpoints
        - Ensure middleware doesn't log sensitive request data
    
    Testing:
        ```bash
        # Test with curl to see timing header
        curl -v http://localhost:8000/items/foo
        
        # Response will include:
        # X-Process-Time: 0.001234
        ```
    
    Common Patterns:
        - Combine with other monitoring middleware
        - Use timing data for automatic scaling decisions
        - Implement circuit breakers based on response times
        - Create performance budgets and alerting thresholds
    """
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Root endpoint for basic application health checking
@app.get("/")
async def read_root():
    """
    Root endpoint providing basic application status and welcome message.
    
    This simple endpoint serves as a health check and demonstrates how
    middleware processes requests to different types of endpoints. The
    middleware timing header will show the minimal processing time for
    this lightweight endpoint.
    
    Returns:
        dict: Simple welcome message confirming service availability
    
    Response Format:
        ```json
        {
            "message": "Hello World"
        }
        ```
    
    Middleware Interaction:
        - Demonstrates minimal processing time measurement
        - Shows middleware execution for simple GET requests
        - Provides baseline timing for performance comparison
        - Includes X-Process-Time header showing endpoint efficiency
    
    Use Cases:
        - Health checks for load balancers and monitoring systems
        - Service discovery and availability verification
        - Performance baseline for middleware timing comparison
        - Integration testing and endpoint accessibility validation
    
    Example Requests:
        ```bash
        # Basic curl request
        curl http://localhost:8000/
        
        # Check response headers including timing
        curl -v http://localhost:8000/
        
        # Expected response headers include:
        # X-Process-Time: 0.000123 (very low for simple endpoint)
        ```
    
    Performance Characteristics:
        - Extremely fast execution (microseconds)
        - No database operations or external dependencies
        - Minimal memory allocation
        - Ideal for performance baseline measurements
        - Useful for testing middleware overhead
    
    Production Usage:
        ```python
        @app.get("/", tags=["health"])
        async def read_root():
            return {
                "message": "Service is running",
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "version": "1.0.0"
            }
        ```
    
    Monitoring Integration:
        - Use for uptime monitoring and alerting
        - Track response times as service health indicator
        - Include in automated testing suites
        - Monitor for availability from multiple regions
    """
    return {"message": "Hello World"}


# Item retrieval endpoint with path parameter validation
@app.get("/items/{item_id}")
async def read_item(item_id: str):
    """
    Retrieve a specific item by its unique identifier.
    
    This endpoint demonstrates how middleware measures processing time
    for endpoints that include path parameters, data lookup operations,
    and conditional response logic. The timing will vary based on whether
    the item exists and the complexity of the lookup operation.
    
    Args:
        item_id (str): The unique identifier for the item to retrieve.
                      Must match a key in the items data store.
    
    Returns:
        dict: Either the item data if found, or an error message if not found
    
    Response Formats:
        Success (200):
        ```json
        {
            "name": "The Foo Wrestlers"
        }
        ```
        
        Not Found (200 with error):
        ```json
        {
            "error": "Item not found"
        }
        ```
    
    Path Parameter Processing:
        - FastAPI automatically extracts item_id from URL path
        - No validation constraints applied (accepts any string)
        - Middleware timing includes path parameter extraction
        - URL encoding/decoding handled automatically by FastAPI
    
    Data Lookup Logic:
        - Performs dictionary lookup operation on items store
        - O(1) average time complexity for hash table lookup
        - Returns actual item data if key exists
        - Returns error message if key doesn't exist
        - No exception raising for missing items (graceful handling)
    
    Middleware Timing Analysis:
        - Fast lookups: ~0.0001-0.001 seconds for existing items
        - Similar timing: for non-existent items due to simple logic
        - Includes time for: path parsing, lookup, response serialization
        - Compare with POST endpoint timing to see relative performance
    
    Example Requests:
        ```bash
        # Retrieve existing item
        curl http://localhost:8000/items/foo
        # Response: {"name": "The Foo Wrestlers"}
        # X-Process-Time: ~0.001 seconds
        
        # Try non-existent item
        curl http://localhost:8000/items/nonexistent
        # Response: {"error": "Item not found"}
        # X-Process-Time: Similar to existing item
        
        # Check timing header
        curl -v http://localhost:8000/items/foo | grep X-Process-Time
        ```
    
    Production Enhancements:
        ```python
        @app.get("/items/{item_id}", response_model=ItemResponse)
        async def read_item(item_id: str = Path(..., min_length=1, max_length=50)):
            # Database lookup with proper error handling
            try:
                item = await database.fetch_one(
                    "SELECT * FROM items WHERE id = :item_id",
                    {"item_id": item_id}
                )
                
                if not item:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Item with id '{item_id}' not found"
                    )
                
                return ItemResponse(**item)
                
            except DatabaseError as e:
                logger.error(f"Database error retrieving item {item_id}: {e}")
                raise HTTPException(
                    status_code=500,
                    detail="Internal server error"
                )
        ```
    
    Error Handling Considerations:
        - Current implementation returns 200 status for missing items
        - Production should use proper HTTP status codes (404 for not found)
        - Consider implementing proper exception handling
        - Add logging for monitoring missing item requests
    
    Performance Monitoring:
        - Track timing patterns for different item_id patterns
        - Monitor for frequently requested vs. missing items
        - Use timing data to optimize data storage strategy
        - Identify slow lookups that might indicate performance issues
    
    Security Considerations:
        - Validate item_id to prevent injection attacks
        - Implement rate limiting for item lookup endpoints
        - Consider access control if items have privacy requirements
        - Log suspicious access patterns to non-existent items
    
    Caching Opportunities:
        - Cache frequently accessed items to reduce lookup time
        - Implement cache-aside pattern for item retrieval
        - Use middleware timing to identify cache hit/miss performance
        - Consider adding cache headers for client-side caching
    
    Testing Examples:
        ```python
        def test_read_existing_item():
            response = client.get("/items/foo")
            assert response.status_code == 200
            assert response.json() == {"name": "The Foo Wrestlers"}
            assert "X-Process-Time" in response.headers
        
        def test_read_nonexistent_item():
            response = client.get("/items/missing")
            assert response.status_code == 200
            assert response.json() == {"error": "Item not found"}
        ```
    """
    if item_id in items:
        return items[item_id]
    return {"error": "Item not found"}


# Item creation endpoint demonstrating POST request middleware interaction
@app.post("/items/")
async def create_item(item: Item):
    """
    Create a new item in the data store.
    
    This endpoint demonstrates how middleware measures processing time for
    POST requests that include request body parsing, Pydantic model validation,
    data transformation, and storage operations. The timing will be higher
    than GET requests due to the additional processing steps.
    
    Args:
        item (Item): Pydantic model containing item data from request body.
                    Automatically parsed and validated by FastAPI.
    
    Returns:
        Item: The created item object, confirming successful creation
    
    Request Body Format:
        ```json
        {
            "name": "laptop",
            "description": "High-performance laptop for development"
        }
        ```
    
    Response Format:
        ```json
        {
            "name": "laptop",
            "description": "High-performance laptop for development"
        }
        ```
    
    Processing Steps (All Measured by Middleware):
        1. HTTP request body parsing and JSON deserialization
        2. Pydantic model validation and type conversion
        3. Business logic execution (data storage)
        4. Response model serialization and JSON encoding
        5. HTTP response generation and header addition
    
    Middleware Timing Analysis:
        - Slower than GET requests due to request body processing
        - Includes time for: JSON parsing, validation, model_dump(), storage
        - Typical timing: ~0.002-0.010 seconds depending on data size
        - Compare with GET endpoint to see processing overhead
        - Validation errors would show different timing patterns
    
    Data Storage Logic:
        - Uses item.name as the dictionary key for storage
        - Converts Pydantic model to dictionary using model_dump()
        - Overwrites existing items with same name (no duplicate checking)
        - Stores complete item data including optional description
    
    Example Requests:
        ```bash
        # Create item with description
        curl -X POST "http://localhost:8000/items/" \
             -H "Content-Type: application/json" \
             -d '{"name": "laptop", "description": "Development machine"}'
        
        # Create item without description
        curl -X POST "http://localhost:8000/items/" \
             -H "Content-Type: application/json" \
             -d '{"name": "mouse"}'
        
        # Check timing header
        curl -v -X POST "http://localhost:8000/items/" \
             -H "Content-Type: application/json" \
             -d '{"name": "keyboard"}' | grep X-Process-Time
        ```
    
    Validation Behavior:
        - Automatic type validation via Pydantic
        - Required field validation (name must be provided)
        - Optional field handling (description defaults to None)
        - JSON schema validation for request body structure
        - HTTP 422 errors for validation failures (handled by FastAPI)
    
    Production Enhancements:
        ```python
        @app.post("/items/", response_model=ItemResponse, status_code=201)
        async def create_item(
            item: ItemCreate,
            background_tasks: BackgroundTasks,
            db: Session = Depends(get_db)
        ):
            # Check for duplicate names
            existing_item = db.query(ItemModel).filter(
                ItemModel.name == item.name
            ).first()
            
            if existing_item:
                raise HTTPException(
                    status_code=409,
                    detail=f"Item with name '{item.name}' already exists"
                )
            
            # Create database record
            try:
                db_item = ItemModel(**item.model_dump())
                db.add(db_item)
                db.commit()
                db.refresh(db_item)
                
                # Add background task for indexing or notifications
                background_tasks.add_task(
                    index_item_for_search, 
                    db_item.id
                )
                
                logger.info(f"Created item: {db_item.name}")
                return ItemResponse.from_orm(db_item)
                
            except IntegrityError as e:
                db.rollback()
                logger.error(f"Database error creating item: {e}")
                raise HTTPException(
                    status_code=500,
                    detail="Failed to create item"
                )
        ```
    
    Error Handling:
        - Pydantic validation errors return 422 status automatically
        - No duplicate checking in current implementation
        - Missing error handling for storage failures
        - Consider adding business logic validation
    
    Performance Considerations:
        - Request body size affects parsing time
        - Pydantic validation time scales with model complexity
        - Storage operation time depends on data store type
        - Consider async database operations for production
        - Monitor validation timing for complex models
    
    Security Features:
        - Automatic input validation via Pydantic
        - Type safety prevents common injection attacks
        - Consider additional business logic validation
        - Implement rate limiting for creation endpoints
        - Add authentication/authorization for production use
    
    Testing Examples:
        ```python
        def test_create_item():
            item_data = {"name": "test_item", "description": "Test description"}
            response = client.post("/items/", json=item_data)
            assert response.status_code == 200
            assert response.json() == item_data
            assert "X-Process-Time" in response.headers
            
            # Verify item was stored
            get_response = client.get("/items/test_item")
            assert get_response.json()["name"] == "test_item"
        
        def test_create_item_validation_error():
            # Missing required name field
            response = client.post("/items/", json={"description": "No name"})
            assert response.status_code == 422
        ```
    
    Monitoring Insights:
        - Track creation timing trends over time
        - Monitor validation error rates and patterns
        - Identify slow creation operations
        - Use timing data for capacity planning
        - Alert on unusually slow creation times
    
    Integration Patterns:
        - Combine with authentication middleware
        - Add request logging middleware
        - Implement rate limiting middleware
        - Use with background task processing
        - Integrate with event-driven architectures
    """
    items[item.name] = item.model_dump()
    return item