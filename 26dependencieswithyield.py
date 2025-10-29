"""
FastAPI Dependencies with Yield Pattern - Lesson 26

This module demonstrates the advanced dependency injection pattern using yield
for resource management in FastAPI. The yield pattern is essential for handling
resources that need proper cleanup, such as database connections, file handles,
or any resources requiring setup and teardown.

Key Concepts:
- Dependency injection with yield keyword
- Resource lifecycle management (setup/teardown)
- Context managers for dependencies
- Database session management patterns
- Automatic resource cleanup
- Exception handling in dependencies

Advanced Features:
- Try/finally blocks in dependencies
- Session-based transaction handling
- Resource pooling concepts
- Memory management patterns
- Production-ready dependency patterns

Real-world Applications:
- Database connection management
- File handle management
- Cache connections (Redis, Memcached)
- External API client management
- Logging context management
- Request-scoped resource allocation

Author: FastAPI Learning Series
Lesson: 26 - Dependencies with Yield Pattern
"""

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Annotated

app = FastAPI(
    title="Dependencies with Yield API",
    description="Advanced dependency injection using yield pattern for resource management",
    version="1.0.0"
)

# Pydantic model for item representation
class Item(BaseModel):
    """
    Pydantic model representing an item in our inventory system.
    
    This model demonstrates data validation and serialization in the context
    of dependency injection with yield patterns. Each item has basic properties
    that are validated automatically by FastAPI.
    
    Attributes:
        name (str): The name/title of the item. Must be a non-empty string.
        price (float): The price of the item in currency units. Must be a valid float.
    
    Examples:
        >>> item = Item(name="Laptop", price=999.99)
        >>> print(item.name)
        'Laptop'
        >>> print(item.price)
        999.99
        
        >>> # Invalid data will raise validation errors
        >>> Item(name="", price="invalid")  # Will raise ValidationError
    
    Production Notes:
        - In real applications, add more validation (min/max values, regex patterns)
        - Consider using Decimal for monetary values instead of float
        - Add description, category, and other relevant fields
        - Implement custom validators for business logic
    """
    name: str
    price: float

# Simple in-memory database simulation
items_db: Dict[int, Item] = {}
next_id = 1

# Simulated database session class (mimics real database drivers)
class DBSession:
    """
    Simulated database session class that demonstrates resource lifecycle management.
    
    This class mimics real database session objects (like SQLAlchemy Session,
    asyncpg Connection, etc.) to demonstrate proper resource management using
    the yield pattern in FastAPI dependencies.
    
    In production applications, this would be replaced by actual database
    connection objects that need proper initialization and cleanup.
    
    Attributes:
        connected (bool): Flag indicating if the session is active
        transaction_count (int): Counter for operations performed in this session
    
    Methods:
        close(): Properly closes the database session and releases resources
    
    Examples:
        >>> session = DBSession()
        Database connection established
        >>> session.connected
        True
        >>> session.transaction_count
        0
        >>> session.close()
        Database connection closed
    
    Production Patterns:
        - Replace with SQLAlchemy Session: sessionmaker(bind=engine)()
        - Use asyncpg for async PostgreSQL: await asyncpg.connect(dsn)
        - Implement connection pooling for better performance
        - Add transaction rollback on exceptions
        - Include connection health checks
        - Implement retry logic for failed connections
    """
    def __init__(self):
        """
        Initialize a new database session.
        
        In real applications, this would:
        - Establish database connection
        - Begin transaction if needed
        - Set up session configuration
        - Initialize connection pooling
        """
        self.connected = True
        self.transaction_count = 0
        print("Database connection established")
    
    def close(self):
        """
        Close the database session and clean up resources.
        
        This method ensures proper cleanup of database resources.
        In real applications, this would:
        - Commit pending transactions
        - Close database connections
        - Return connections to pool
        - Clean up session state
        - Log session statistics
        """
        self.connected = False
        print("Database connection closed")

async def get_db():
    """
    Database session dependency using yield pattern for proper resource management.
    
    This dependency demonstrates the advanced yield pattern in FastAPI, which ensures
    proper setup and teardown of resources. The yield keyword creates a context manager
    that guarantees the finally block executes even if an exception occurs.
    
    The yield pattern is essential for:
    - Database connection management
    - File handle management  
    - Cache connections
    - External API clients
    - Any resource requiring cleanup
    
    Flow:
    1. Setup: Create database session
    2. Yield: Provide session to endpoint
    3. Cleanup: Always close session (even on exceptions)
    
    Args:
        None (this is a dependency function)
    
    Yields:
        DBSession: Active database session for use in endpoints
    
    Examples:
        # Used as dependency in endpoints:
        @app.get("/items/")
        async def get_items(db: Annotated[DBSession, Depends(get_db)]):
            # db is automatically injected and cleaned up
            return perform_query(db)
    
    Production Implementation:
        ```python
        async def get_db():
            # SQLAlchemy example
            session = SessionLocal()
            try:
                yield session
            finally:
                session.close()
                
        # Or with asyncpg
        async def get_db():
            conn = await asyncpg.connect(DATABASE_URL)
            try:
                yield conn
            finally:
                await conn.close()
        ```
    
    Exception Handling:
        - If endpoint raises exception, finally block still executes
        - Session is always closed, preventing resource leaks
        - Transactions can be rolled back in finally block if needed
        
    Notes:
        - The yield keyword makes this function a generator
        - FastAPI handles the generator lifecycle automatically
        - Code before yield runs before the endpoint
        - Code after yield (in finally) runs after the endpoint
        - This pattern prevents resource leaks in production
    """
    db = DBSession()
    try:
        yield db
    finally:
        db.close()

# FastAPI endpoints demonstrating dependencies with yield

@app.post("/items/")
async def create_item(item: Item, db: Annotated[DBSession, Depends(get_db)]) -> Dict:
    """
    Create a new item in the database using dependency injection with yield.
    
    This endpoint demonstrates how the yield pattern ensures proper database
    session management. The session is automatically created before the endpoint
    runs and cleaned up after, regardless of success or failure.
    
    Args:
        item (Item): Pydantic model containing item data to create
        db (DBSession): Database session injected via dependency with yield pattern
    
    Returns:
        Dict: Created item data including the assigned ID
    
    Raises:
        HTTPException: If item creation fails (in production)
        ValidationError: If item data is invalid (handled by FastAPI)
    
    Examples:
        POST /items/
        {
            "name": "Laptop",
            "price": 999.99
        }
        
        Response:
        {
            "id": 1,
            "name": "Laptop", 
            "price": 999.99
        }
    
    Database Session Lifecycle:
        1. get_db() creates DBSession
        2. Session is yielded to this endpoint
        3. Endpoint uses session for operations
        4. Session is automatically closed after endpoint completes
        5. Even if exception occurs, finally block ensures cleanup
    
    Production Considerations:
        - Add input validation beyond Pydantic
        - Implement proper error handling
        - Use database transactions for data integrity
        - Add logging for audit trails
        - Consider rate limiting for this endpoint
        - Implement proper ID generation (UUID, etc.)
        - Add duplicate detection logic
    """
    global next_id
    db.transaction_count += 1  # Track operations in this session
    item_id = next_id
    items_db[item_id] = item
    next_id += 1
    return {"id": item_id, **item.model_dump()}

@app.get("/items/")
async def get_items(db: Annotated[DBSession, Depends(get_db)]) -> Dict[int, Item]:
    """
    Retrieve all items from the database using dependency injection with yield.
    
    This endpoint shows how multiple endpoints can share the same dependency
    pattern, each getting their own database session that's properly managed
    through the yield pattern.
    
    Args:
        db (DBSession): Database session injected via dependency with yield pattern
    
    Returns:
        Dict[int, Item]: Dictionary mapping item IDs to Item objects
    
    Examples:
        GET /items/
        
        Response:
        {
            "1": {
                "name": "Laptop",
                "price": 999.99
            },
            "2": {
                "name": "Mouse", 
                "price": 29.99
            }
        }
    
    Database Session Lifecycle:
        1. New DBSession created for this request
        2. Session yielded to endpoint
        3. Transaction count incremented
        4. Data retrieved from database
        5. Session automatically closed after response
    
    Production Patterns:
        ```python
        async def get_items(
            db: Annotated[AsyncSession, Depends(get_db)],
            skip: int = 0,
            limit: int = 100
        ):
            query = select(Item).offset(skip).limit(limit)
            result = await db.execute(query)
            return result.scalars().all()
        ```
    
    Performance Considerations:
        - Add pagination for large datasets
        - Implement caching for frequently accessed data
        - Use database indexes for better query performance
        - Consider connection pooling for high traffic
        - Add query optimization and monitoring
    """
    db.transaction_count += 1  # Track operations in this session
    return items_db

# Application startup messages
print("🚀 FastAPI Dependencies with Yield - Ready!")
print("💡 Key Features:")
print("   ✅ Yield pattern for resource management")
print("   ✅ Automatic session cleanup")
print("   ✅ Exception-safe resource handling")
print("   ✅ Production-ready dependency patterns")
print("📚 Endpoints:")
print("   POST /items/ - Create item with managed database session")
print("   GET /items/  - List items with automatic session cleanup")
print("🔧 Advanced concepts: Setup/teardown, context managers, resource pooling")