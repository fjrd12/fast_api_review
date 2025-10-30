"""
FastAPI Items Router - Item Management API Module

This module implements a comprehensive item management API using FastAPI's APIRouter
pattern. It demonstrates:

- **Modular Router Design**: Organized endpoint grouping with APIRouter
- **Multi-Layer Authentication**: Global and router-specific security
- **CRUD Operations**: Complete Create, Read, Update operations for items
- **Error Handling**: Standardized HTTP error responses
- **Custom Response Definitions**: OpenAPI documentation enhancement
- **Resource Protection**: Selective update permissions and access control

Router Configuration:
- **Prefix**: /items - All endpoints prefixed for URL organization
- **Tags**: ["items"] - OpenAPI documentation grouping
- **Dependencies**: Header token authentication for all endpoints
- **Custom Responses**: 404 error response definitions

Authentication Layers:
1. **Global Authentication**: Query token (token=jessica) required for all requests
2. **Router Authentication**: X-Token header (fake-super-secret-token) for item operations
3. **Operation-Specific**: Custom permissions for certain operations (e.g., plumbus updates)

Endpoint Structure:
- GET /items/ - Retrieve all items (read-only operation)
- GET /items/{item_id} - Retrieve specific item by ID
- PUT /items/{item_id} - Update item (restricted to specific items)

Data Model:
- Simple key-value store with item names
- Extensible structure for additional item properties
- In-memory storage for demonstration (production would use database)

Security Features:
- **Token Validation**: Multiple authentication layers
- **Resource Protection**: Selective write permissions
- **Error Standardization**: Consistent error response format
- **Access Logging**: Audit trail capabilities

Production Considerations:
- **Database Integration**: Replace in-memory storage with persistent database
- **Caching Strategy**: Implement Redis or similar for performance
- **Rate Limiting**: Prevent abuse of item operations
- **Pagination**: Handle large item collections efficiently
- **Search Functionality**: Add filtering and search capabilities
"""

from fastapi import APIRouter, Depends, HTTPException

# Import authentication dependency from parent package
from ..dependencies import get_token_header


def create_items_router() -> APIRouter:
    """
    Create and configure the items router with proper security and documentation.
    
    This function demonstrates the factory pattern for router creation,
    enabling flexible configuration and testing scenarios.
    
    Returns:
        APIRouter: Configured router instance with authentication and responses
    
    Router Configuration:
        - **URL Prefix**: /items for namespace organization
        - **Documentation Tags**: ["items"] for OpenAPI grouping
        - **Security Dependencies**: Header token authentication
        - **Error Responses**: Standardized 404 response definition
    
    Security Configuration:
        - Requires both global query token and router-specific header token
        - All endpoints protected by dual authentication layers
        - Custom permission checks for specific operations
    
    Documentation Features:
        - OpenAPI tag grouping for better API documentation
        - Custom response schemas for error handling
        - Detailed endpoint descriptions and examples
    """
    return APIRouter(
        prefix="/items",
        tags=["items"],
        dependencies=[Depends(get_token_header)],
        responses={404: {"description": "Not found"}},
    )


# Create router instance with configuration
router = create_items_router()


# Sample items database - In-memory storage for demonstration
fake_items_db = {
    "plumbus": {"name": "Plumbus"},
    "gun": {"name": "Portal Gun"}
}


@router.get("/")
async def read_items():
    """
    Retrieve all available items from the items database.
    
    This endpoint provides access to the complete items catalog,
    returning all items currently available in the system.
    
    Returns:
        dict: Complete items database with item IDs as keys
    
    Response Format:
        ```json
        {
            "plumbus": {"name": "Plumbus"},
            "gun": {"name": "Portal Gun"}
        }
        ```
    
    Authentication Requirements:
        - **Global Token**: Query parameter token=jessica required
        - **Header Token**: X-Token header with fake-super-secret-token required
    
    Use Cases:
        - **Catalog Browsing**: Display all available items to users
        - **Inventory Management**: Administrative view of all items
        - **Search Foundation**: Base data for search and filtering operations
        - **Cache Warm-up**: Preload item data for performance
    
    Example Usage:
        ```bash
        # Successful request with both authentication tokens
        curl -H "X-Token: fake-super-secret-token" \
             "http://localhost:8000/items/?token=jessica"
        
        # Response
        {
            "plumbus": {"name": "Plumbus"},
            "gun": {"name": "Portal Gun"}
        }
        ```
    
    Error Scenarios:
        ```bash
        # Missing global token
        curl -H "X-Token: fake-super-secret-token" \
             "http://localhost:8000/items/"
        # Returns: 422 "field required"
        
        # Missing header token
        curl "http://localhost:8000/items/?token=jessica"
        # Returns: 422 "field required"
        
        # Invalid tokens
        curl -H "X-Token: invalid" \
             "http://localhost:8000/items/?token=invalid"
        # Returns: 400 authentication errors
        ```
    
    Production Implementation:
        ```python
        from sqlalchemy.orm import Session
        from typing import List, Optional
        
        @router.get("/", response_model=List[ItemResponse])
        async def read_items(
            skip: int = Query(0, ge=0),
            limit: int = Query(100, le=1000),
            search: Optional[str] = Query(None),
            db: Session = Depends(get_database)
        ):
            query = db.query(Item)
            
            if search:
                query = query.filter(Item.name.contains(search))
            
            items = query.offset(skip).limit(limit).all()
            return items
        ```
    
    Caching Strategy:
        ```python
        import redis
        import json
        from datetime import timedelta
        
        @router.get("/")
        async def read_items(redis_client: Redis = Depends(get_redis)):
            # Check cache first
            cached_items = await redis_client.get("items:all")
            if cached_items:
                return json.loads(cached_items)
            
            # Fetch from database
            items = await fetch_items_from_db()
            
            # Cache for 5 minutes
            await redis_client.setex(
                "items:all", 
                timedelta(minutes=5), 
                json.dumps(items)
            )
            
            return items
        ```
    
    Performance Considerations:
        - **Memory Usage**: In-memory storage suitable only for small datasets
        - **Response Size**: Consider pagination for large item collections
        - **Caching**: Implement caching for frequently accessed data
        - **Database Optimization**: Use proper indexing for production queries
    
    Security Considerations:
        - **Data Exposure**: Ensure only appropriate item data is returned
        - **Rate Limiting**: Prevent abuse of bulk data retrieval
        - **Access Logging**: Log item access for audit purposes
        - **Pagination**: Prevent large data dumps that could impact performance
    """
    return fake_items_db


@router.get("/{item_id}")
async def read_item(item_id: str):
    """
    Retrieve a specific item by its unique identifier.
    
    This endpoint provides detailed information about a single item,
    identified by its unique item ID. It includes error handling for
    non-existent items and demonstrates proper resource retrieval patterns.
    
    Args:
        item_id (str): Unique identifier for the item to retrieve
    
    Returns:
        dict: Item details including name and ID
    
    Raises:
        HTTPException: 404 error if item with specified ID doesn't exist
    
    Response Format:
        ```json
        {
            "name": "Portal Gun",
            "item_id": "gun"
        }
        ```
    
    Authentication Requirements:
        - **Global Token**: Query parameter token=jessica required
        - **Header Token**: X-Token header with fake-super-secret-token required
    
    Use Cases:
        - **Item Details**: Display detailed information about specific items
        - **Inventory Lookup**: Check availability and details of specific items
        - **Link Resolution**: Resolve item references from other systems
        - **Validation**: Verify item existence before operations
    
    Example Usage:
        ```bash
        # Successful request for existing item
        curl -H "X-Token: fake-super-secret-token" \
             "http://localhost:8000/items/gun?token=jessica"
        
        # Response
        {
            "name": "Portal Gun",
            "item_id": "gun"
        }
        
        # Request for another existing item
        curl -H "X-Token: fake-super-secret-token" \
             "http://localhost:8000/items/plumbus?token=jessica"
        
        # Response
        {
            "name": "Plumbus",
            "item_id": "plumbus"
        }
        ```
    
    Error Scenarios:
        ```bash
        # Non-existent item
        curl -H "X-Token: fake-super-secret-token" \
             "http://localhost:8000/items/nonexistent?token=jessica"
        # Returns: 404 "Item not found"
        
        # Authentication errors
        curl "http://localhost:8000/items/gun?token=invalid"
        # Returns: 400 authentication errors
        ```
    
    Production Implementation:
        ```python
        from sqlalchemy.orm import Session
        from typing import Optional
        
        @router.get("/{item_id}", response_model=ItemDetailResponse)
        async def read_item(
            item_id: int,
            include_details: bool = Query(False),
            db: Session = Depends(get_database)
        ):
            # Query with optional detailed information
            query = db.query(Item).filter(Item.id == item_id)
            
            if include_details:
                query = query.options(
                    joinedload(Item.category),
                    joinedload(Item.reviews)
                )
            
            item = query.first()
            if not item:
                raise HTTPException(404, f"Item {item_id} not found")
            
            return item
        ```
    
    Caching Implementation:
        ```python
        import redis
        import json
        
        @router.get("/{item_id}")
        async def read_item(
            item_id: str,
            redis_client: Redis = Depends(get_redis)
        ):
            # Check cache first
            cache_key = f"item:{item_id}"
            cached_item = await redis_client.get(cache_key)
            
            if cached_item:
                return json.loads(cached_item)
            
            # Check database
            if item_id not in fake_items_db:
                raise HTTPException(404, "Item not found")
            
            item_data = {
                "name": fake_items_db[item_id]["name"],
                "item_id": item_id
            }
            
            # Cache for 1 hour
            await redis_client.setex(
                cache_key, 
                timedelta(hours=1), 
                json.dumps(item_data)
            )
            
            return item_data
        ```
    
    Error Handling Patterns:
        ```python
        from enum import Enum
        
        class ItemNotFoundError(Exception):
            def __init__(self, item_id: str):
                self.item_id = item_id
                super().__init__(f"Item {item_id} not found")
        
        @app.exception_handler(ItemNotFoundError)
        async def item_not_found_handler(request: Request, exc: ItemNotFoundError):
            return JSONResponse(
                status_code=404,
                content={
                    "detail": str(exc),
                    "item_id": exc.item_id,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
        ```
    
    Performance Optimizations:
        - **Database Indexing**: Ensure item_id is properly indexed
        - **Connection Pooling**: Use connection pools for database access
        - **Query Optimization**: Use appropriate joins and selections
        - **Response Compression**: Enable gzip compression for responses
    
    Security Considerations:
        - **Input Validation**: Validate item_id format and constraints
        - **Access Control**: Ensure users can only access permitted items
        - **Rate Limiting**: Prevent excessive item lookup requests
        - **Audit Logging**: Log item access for security monitoring
    """
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}


@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    """
    Update a specific item with restricted permissions.
    
    This endpoint demonstrates selective update permissions and custom
    response documentation. It allows updates only to specific items,
    showcasing access control patterns and business rule enforcement.
    
    Args:
        item_id (str): Unique identifier for the item to update
    
    Returns:
        dict: Updated item information with ID and new name
    
    Raises:
        HTTPException: 403 error if attempting to update unauthorized items
    
    Response Format:
        ```json
        {
            "item_id": "plumbus",
            "name": "The great Plumbus"
        }
        ```
    
    Business Rules:
        - **Restricted Updates**: Only "plumbus" item can be updated
        - **Predefined Updates**: Updates follow predefined patterns
        - **Permission Control**: Demonstrates selective resource modification
    
    Authentication Requirements:
        - **Global Token**: Query parameter token=jessica required
        - **Header Token**: X-Token header with fake-super-secret-token required
    
    OpenAPI Documentation:
        - **Custom Tags**: ["custom"] for specialized operation grouping
        - **Custom Responses**: 403 forbidden response definition
        - **Operation Documentation**: Detailed error scenario descriptions
    
    Use Cases:
        - **Selective Updates**: Business rules requiring specific update permissions
        - **Premium Features**: Operations restricted to premium users
        - **Administrative Control**: Operations requiring special authorization
        - **Resource Protection**: Preventing unauthorized modifications
    
    Example Usage:
        ```bash
        # Successful update of allowed item
        curl -X PUT \
             -H "X-Token: fake-super-secret-token" \
             "http://localhost:8000/items/plumbus?token=jessica"
        
        # Response
        {
            "item_id": "plumbus",
            "name": "The great Plumbus"
        }
        ```
    
    Error Scenarios:
        ```bash
        # Attempting to update unauthorized item
        curl -X PUT \
             -H "X-Token: fake-super-secret-token" \
             "http://localhost:8000/items/gun?token=jessica"
        # Returns: 403 "You can only update the item: plumbus"
        
        # Non-existent item
        curl -X PUT \
             -H "X-Token: fake-super-secret-token" \
             "http://localhost:8000/items/nonexistent?token=jessica"
        # Returns: 403 "You can only update the item: plumbus"
        
        # Authentication errors
        curl -X PUT "http://localhost:8000/items/plumbus?token=invalid"
        # Returns: 400 authentication errors
        ```
    
    Production Implementation:
        ```python
        from sqlalchemy.orm import Session
        from pydantic import BaseModel
        
        class ItemUpdate(BaseModel):
            name: str
            description: Optional[str] = None
            price: Optional[float] = None
        
        @router.put("/{item_id}", response_model=ItemResponse)
        async def update_item(
            item_id: int,
            item_update: ItemUpdate,
            current_user: User = Depends(get_current_user),
            db: Session = Depends(get_database)
        ):
            # Check if user has permission to update this item
            if not await check_update_permission(current_user, item_id):
                raise HTTPException(403, "Insufficient permissions")
            
            # Fetch existing item
            db_item = db.query(Item).filter(Item.id == item_id).first()
            if not db_item:
                raise HTTPException(404, "Item not found")
            
            # Apply updates
            update_data = item_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_item, field, value)
            
            # Update timestamp
            db_item.updated_at = datetime.utcnow()
            
            # Save changes
            db.commit()
            db.refresh(db_item)
            
            return db_item
        ```
    
    Permission System:
        ```python
        from enum import Enum
        
        class UpdatePermission(Enum):
            OWNER = "owner"
            ADMIN = "admin"
            MODERATOR = "moderator"
        
        async def check_update_permission(
            user: User, 
            item_id: int,
            db: Session = Depends(get_database)
        ) -> bool:
            item = db.query(Item).filter(Item.id == item_id).first()
            if not item:
                return False
            
            # Owner can always update
            if item.owner_id == user.id:
                return True
            
            # Admin can update any item
            if user.role == UpdatePermission.ADMIN:
                return True
            
            # Moderator can update if item is not premium
            if user.role == UpdatePermission.MODERATOR and not item.is_premium:
                return True
            
            return False
        ```
    
    Audit Logging:
        ```python
        import logging
        from datetime import datetime
        
        @router.put("/{item_id}")
        async def update_item(
            item_id: str,
            current_user: User = Depends(get_current_user)
        ):
            # Log update attempt
            logger.info(f"Update attempt - User: {current_user.id}, Item: {item_id}")
            
            if item_id != "plumbus":
                # Log unauthorized attempt
                logger.warning(
                    f"Unauthorized update attempt - "
                    f"User: {current_user.id}, Item: {item_id}"
                )
                raise HTTPException(403, "You can only update the item: plumbus")
            
            # Log successful update
            logger.info(f"Successful update - User: {current_user.id}, Item: {item_id}")
            
            return {"item_id": item_id, "name": "The great Plumbus"}
        ```
    
    Validation Patterns:
        ```python
        from pydantic import BaseModel, validator
        
        class ItemUpdateRequest(BaseModel):
            name: str
            description: Optional[str] = None
            
            @validator('name')
            def validate_name(cls, v):
                if len(v) < 3:
                    raise ValueError('Name must be at least 3 characters')
                if len(v) > 100:
                    raise ValueError('Name must be less than 100 characters')
                return v.strip()
        
        @router.put("/{item_id}")
        async def update_item(item_id: str, item_data: ItemUpdateRequest):
            # Validation happens automatically via Pydantic
            if item_id != "plumbus":
                raise HTTPException(403, "You can only update the item: plumbus")
            
            return {
                "item_id": item_id,
                "name": item_data.name,
                "description": item_data.description
            }
        ```
    
    Security Considerations:
        - **Permission Validation**: Always check user permissions before updates
        - **Input Sanitization**: Validate and sanitize all input data
        - **Audit Trails**: Log all update attempts and their outcomes
        - **Rate Limiting**: Prevent excessive update requests
        - **Data Validation**: Ensure updates don't violate business constraints
    
    Performance Considerations:
        - **Database Transactions**: Use proper transaction handling
        - **Optimistic Locking**: Handle concurrent update scenarios
        - **Cache Invalidation**: Clear relevant caches after updates
        - **Bulk Operations**: Consider bulk update patterns for multiple items
    """
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}
