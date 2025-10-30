"""
FastAPI SQL Databases with SQLModel - Lesson 33

This module demonstrates comprehensive database integration using SQLModel,
which combines SQLAlchemy's power with Pydantic's validation in a unified
framework. SQLModel provides type-safe database operations, automatic
API documentation, and seamless integration between database models and
API request/response schemas.

SQLModel Overview:
    SQLModel is created by the same author as FastAPI and Pydantic, designed
    to reduce code duplication and provide a single source of truth for
    database models and API schemas. It leverages Python type hints for
    both database definitions and API validation.

Key Features Demonstrated:
    - Database model definition with SQLModel
    - Multiple model patterns (Base, Table, Public, Create, Update)
    - Database session management with dependency injection
    - CRUD operations with proper error handling
    - Pagination and query optimization
    - Type-safe database operations
    - Automatic API documentation generation

Architecture Patterns:
    - Model inheritance for shared fields and validation
    - Separation of concerns between database and API models
    - Session-per-request pattern for thread safety
    - Lifespan management for database initialization
    - Response model filtering for security and efficiency

Database Design:
    - SQLite for simplicity and portability
    - Indexed fields for query performance
    - Primary key auto-generation
    - Optional fields with proper defaults
    - Type validation at database and API levels

Production Considerations:
    - Connection pooling and session management
    - Database migrations and schema evolution
    - Query optimization and performance monitoring
    - Error handling and transaction management
    - Security best practices for data exposure

Learning Objectives:
    - Understand SQLModel's unified approach to database and API modeling
    - Implement proper CRUD operations with error handling
    - Design secure API models that protect sensitive data
    - Manage database sessions and connections efficiently
    - Build scalable database-driven APIs with FastAPI

Dependencies:
    - SQLModel: Unified database and API modeling
    - FastAPI: High-performance web framework
    - SQLAlchemy: Underlying ORM engine
    - Pydantic: Data validation and serialization

Security Features:
    - Sensitive field exclusion in public models
    - Input validation on all endpoints
    - SQL injection prevention through ORM
    - Proper HTTP status codes for different scenarios

Author: FastAPI Learning Series
Created: 2025-10-30
Framework: SQLModel + FastAPI + SQLAlchemy
Database: SQLite (development), PostgreSQL/MySQL (production)
"""

from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

# Base model containing shared fields and validation rules
class HeroBase(SQLModel):
    """
    Base model for Hero entities containing common fields and validation.
    
    This model serves as the foundation for all Hero-related models,
    providing shared fields and validation logic. It demonstrates the
    SQLModel pattern of using inheritance to reduce code duplication
    and ensure consistency across different model variants.
    
    Attributes:
        name (str): The hero's public name or alias. Indexed for fast queries.
        age (int): The hero's age in years. Indexed for age-based filtering.
    
    Design Patterns:
        - Single source of truth for shared field definitions
        - Consistent validation rules across all Hero models
        - Database indexing for frequently queried fields
        - Type safety with automatic validation
    
    Database Optimization:
        - Both fields are indexed for query performance
        - String fields use appropriate database types
        - Integer fields use efficient storage
    
    Inheritance Benefits:
        - Reduces code duplication across models
        - Ensures consistent field definitions
        - Centralizes validation logic
        - Simplifies maintenance and updates
    
    Usage in SQLModel:
        ```python
        # Used as base for other models
        class Hero(HeroBase, table=True):
            # Additional table-specific fields
            pass
        
        class HeroCreate(HeroBase):
            # Additional creation-specific fields
            pass
        ```
    
    Field Configuration:
        - index=True: Creates database indexes for faster queries
        - Type hints: Provide validation and documentation
        - No defaults: All fields are required in base model
    
    Validation Features:
        - Automatic type validation via Pydantic
        - String length validation (can be added)
        - Age range validation (can be extended)
        - SQL injection prevention through ORM
    """
    name: str = Field(index=True)
    age: int = Field(index=True)    

# Database table model representing the actual Hero entity
class Hero(HeroBase, table=True):
    """
    Main Hero table model representing the database entity.
    
    This model inherits from HeroBase and adds table-specific fields,
    serving as the actual database table definition. The table=True
    parameter tells SQLModel to create a database table for this model.
    
    Attributes:
        id (int): Primary key, auto-generated for new records
        secret_name (str): The hero's real identity, kept confidential
        
    Inherited from HeroBase:
        name (str): Public hero name/alias
        age (int): Hero's age
    
    Database Design:
        - Primary key auto-generation for unique identification
        - Optional secret_name allows heroes without secret identities
        - Inherits indexed fields for query optimization
        - SQLModel generates appropriate SQL schema
    
    Table Configuration:
        - table=True: Creates actual database table
        - Automatic table naming based on class name
        - Inherits all constraints and indexes from base model
        - Supports foreign keys and relationships (can be extended)
    
    Security Considerations:
        - secret_name is sensitive data not exposed in public APIs
        - Primary key provides unique identification
        - Database-level constraints prevent invalid data
        - ORM prevents SQL injection attacks
    
    CRUD Operations:
        - Create: Insert new heroes with auto-generated IDs
        - Read: Query by ID or other fields
        - Update: Modify existing hero data
        - Delete: Remove heroes from database
    
    SQLModel Features:
        - Automatic schema generation
        - Type-safe database operations
        - Integration with FastAPI response models
        - Pydantic validation for all fields
    
    Production Considerations:
        - Add created_at/updated_at timestamps
        - Implement soft deletes if needed
        - Add foreign key relationships
        - Consider data archival strategies
    
    Example Usage:
        ```python
        # Create new hero
        hero = Hero(name="Spider-Man", age=25, secret_name="Peter Parker")
        session.add(hero)
        session.commit()
        
        # Query hero
        hero = session.get(Hero, 1)
        ```
    """
    id: int = Field(default=None, primary_key=True)
    secret_name: str = Field(default=None)

# Public response model for API endpoints (excludes sensitive data)
class HeroPublic(HeroBase):
    """
    Public Hero model for API responses, excluding sensitive information.
    
    This model is used for API responses and public data exposure,
    intentionally excluding the secret_name field to protect hero
    identities. It demonstrates the security pattern of using different
    models for internal storage and public APIs.
    
    Attributes:
        id (int): Hero's unique identifier
        
    Inherited from HeroBase:
        name (str): Public hero name/alias
        age (int): Hero's age
    
    Security Design:
        - Excludes secret_name field for privacy protection
        - Only exposes safe, public information
        - Prevents accidental data leakage
        - Used in all public API endpoints
    
    Response Model Pattern:
        - Dedicated model for API responses
        - Filters out sensitive database fields
        - Maintains consistent API contracts
        - Enables safe data sharing
    
    FastAPI Integration:
        - Used with response_model parameter
        - Automatic JSON serialization
        - OpenAPI documentation generation
        - Type hints for client code generation
    
    Data Transformation:
        - SQLModel automatically converts Hero → HeroPublic
        - Pydantic handles serialization to JSON
        - Type validation ensures data integrity
        - No manual field mapping required
    
    Client Benefits:
        - Clean, consistent API responses
        - Predictable data structure
        - Type safety for frontend applications
        - Automatic documentation in OpenAPI spec
    
    Usage Examples:
        ```python
        # FastAPI endpoint
        @app.get("/heroes/{id}", response_model=HeroPublic)
        def get_hero(id: int):
            hero_db = session.get(Hero, id)
            return hero_db  # Automatic conversion
        
        # Response JSON
        {
            "id": 1,
            "name": "Spider-Man",
            "age": 25
            # secret_name excluded
        }
        ```
    
    Production Considerations:
        - Add computed fields if needed
        - Consider response compression for large datasets
        - Implement field-level permissions
        - Add response caching headers
    """
    id: int = Field(default=None)    

# Input model for hero creation requests
class HeroCreate(HeroBase):
    """
    Input model for creating new heroes via API requests.
    
    This model extends HeroBase with fields specific to hero creation,
    including the secret_name which is required during creation but
    not exposed in public responses. It validates all input data
    before database insertion.
    
    Attributes:
        secret_name (str): The hero's real identity, required for creation
        
    Inherited from HeroBase:
        name (str): Public hero name/alias
        age (int): Hero's age
    
    Creation Workflow:
        1. Client sends POST request with HeroCreate data
        2. FastAPI validates against this model
        3. Data is converted to Hero model for database storage
        4. Response uses HeroPublic model for security
    
    Validation Features:
        - All required fields must be provided
        - Type validation for all attributes
        - Automatic JSON deserialization
        - Pydantic error messages for invalid data
    
    Security Considerations:
        - secret_name is accepted but not returned in responses
        - Input sanitization prevents injection attacks
        - Validation prevents malformed data
        - No direct database field exposure
    
    Request/Response Pattern:
        ```
        Request (HeroCreate):
        {
            "name": "Spider-Man",
            "age": 25,
            "secret_name": "Peter Parker"
        }
        
        Response (HeroPublic):
        {
            "id": 1,
            "name": "Spider-Man",
            "age": 25
            # secret_name excluded
        }
        ```
    
    FastAPI Integration:
        - Used as request body parameter type
        - Automatic validation and error handling
        - OpenAPI schema generation
        - Type hints for development tools
    
    Data Conversion:
        ```python
        # FastAPI automatically handles:
        hero_create = HeroCreate(**request_data)  # Validation
        hero_db = Hero.model_validate(hero_create)  # Conversion
        ```
    
    Error Handling:
        - 422 status for validation errors
        - Detailed error messages for debugging
        - Field-level error reporting
        - Client-friendly error responses
    
    Production Enhancements:
        - Add custom validators for business rules
        - Implement field length restrictions
        - Add password hashing for authentication
        - Include audit fields (created_by, etc.)
    """
    secret_name: str = Field(default=None)

# Update model with optional fields for partial updates
class HeroUpdate(SQLModel):
    """
    Model for partial hero updates using PATCH requests.
    
    This model supports partial updates by making all fields optional,
    allowing clients to update only specific hero attributes without
    requiring all fields. It follows REST API best practices for
    resource modification.
    
    Attributes:
        name (str | None): Optional hero name update
        age (int | None): Optional age update  
        secret_name (str | None): Optional secret identity update
    
    Partial Update Pattern:
        - All fields are optional (None defaults)
        - Only provided fields are updated
        - Existing values preserved for omitted fields
        - PATCH HTTP method for partial updates
    
    Update Workflow:
        1. Client sends PATCH with subset of fields
        2. Model validates provided fields only
        3. exclude_unset=True filters out None values
        4. Only specified fields are updated in database
    
    Flexibility Benefits:
        - Update single fields without affecting others
        - Efficient network usage (send only changes)
        - Atomic updates for specific attributes
        - Client controls update granularity
    
    Usage Example:
        ```python
        # Update only age
        update_data = HeroUpdate(age=26)
        
        # Update name and secret_name
        update_data = HeroUpdate(
            name="Amazing Spider-Man",
            secret_name="Peter Benjamin Parker"
        )
        
        # SQLModel processing
        hero_data = update_data.model_dump(exclude_unset=True)
        # Only includes non-None fields
        ```
    
    Database Integration:
        ```python
        # Efficient update process
        hero_db = session.get(Hero, hero_id)
        hero_data = hero_update.model_dump(exclude_unset=True)
        hero_db.sqlmodel_update(hero_data)
        session.commit()
        ```
    
    Validation Features:
        - Type validation for provided fields
        - None values allowed and ignored
        - Automatic JSON deserialization
        - Error handling for invalid types
    
    Security Considerations:
        - Validate user permissions for field updates
        - Audit trail for sensitive field changes
        - Rate limiting for update operations
        - Input sanitization for all fields
    
    HTTP Status Codes:
        - 200: Successful update with response body
        - 404: Hero not found
        - 422: Validation error in update data
        - 403: Insufficient permissions (if implemented)
    
    Production Enhancements:
        - Add field-level permissions
        - Implement optimistic locking
        - Add validation for business rules
        - Include update timestamps
        - Support bulk updates for efficiency
    
    Client Usage:
        ```javascript
        // Frontend partial update
        fetch(`/heroes/${heroId}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ age: 26 })  // Only update age
        });
        ```
    """
    name: str | None = Field(default=None)
    age: int | None = Field(default=None)
    secret_name: str | None = Field(default=None)

# Database configuration and engine setup
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)
"""
Database engine configuration for SQLite.

This section sets up the database connection using SQLAlchemy's engine
system with SQLite for development simplicity. The configuration handles
thread safety and connection management for FastAPI's async nature.

Configuration Details:
    - sqlite_file_name: Local database file name
    - sqlite_url: SQLAlchemy connection string
    - connect_args: Thread safety configuration for SQLite
    - engine: SQLAlchemy engine instance for all database operations

SQLite Configuration:
    - check_same_thread=False: Allows SQLite usage across threads
    - Local file storage: Simple setup for development
    - No server required: Embedded database solution
    - ACID transactions: Full database transaction support

Production Alternatives:
    PostgreSQL:
        ```python
        DATABASE_URL = "postgresql://user:password@host:port/database"
        engine = create_engine(DATABASE_URL)
        ```
    
    MySQL:
        ```python
        DATABASE_URL = "mysql+pymysql://user:password@host:port/database"
        engine = create_engine(DATABASE_URL)
        ```
    
    SQLServer:
        ```python
        DATABASE_URL = "mssql+pyodbc://user:password@host:port/database?driver=ODBC+Driver+17+for+SQL+Server"
        engine = create_engine(DATABASE_URL)
        ```

Connection Pooling:
    ```python
    engine = create_engine(
        DATABASE_URL,
        pool_size=20,          # Number of connections to maintain
        max_overflow=0,        # Additional connections allowed
        pool_pre_ping=True,    # Validate connections before use
        pool_recycle=300       # Recycle connections every 5 minutes
    )
    ```

Environment Configuration:
    ```python
    import os
    
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
    )
    ```
"""

# Database table creation function
def create_db_and_tables():
    """
    Create all database tables based on SQLModel definitions.
    
    This function uses SQLModel's metadata to create all defined tables
    in the database. It's called during application startup to ensure
    the database schema exists before handling requests.
    
    SQLModel Integration:
        - Reads all models with table=True
        - Generates CREATE TABLE statements
        - Handles indexes, constraints, and relationships
        - Idempotent operation (safe to call multiple times)
    
    Database Operations:
        - Creates tables if they don't exist
        - Preserves existing data during restarts
        - Applies schema changes (in development)
        - Handles foreign key relationships
    
    Usage Context:
        - Called during application startup
        - Ensures database readiness before API requests
        - Development convenience for schema management
        - Production requires proper migration strategy
    
    Production Considerations:
        - Replace with proper database migrations (Alembic)
        - Version control for schema changes
        - Backup strategies before schema modifications
        - Rolling deployment compatibility
    
    Migration Alternative:
        ```python
        # Production migration approach
        from alembic import command
        from alembic.config import Config
        
        def run_migrations():
            alembic_cfg = Config("alembic.ini")
            command.upgrade(alembic_cfg, "head")
        ```
    
    Error Handling:
        - Database connection errors are propagated
        - Schema conflicts may raise exceptions
        - Logging should be added for production use
        - Rollback strategies for failed migrations
    """
    SQLModel.metadata.create_all(engine)

# Database session dependency for request handling
def get_session():
    """
    Database session dependency generator for FastAPI endpoints.
    
    This function creates a database session for each request and ensures
    proper cleanup after the request completes. It implements the
    session-per-request pattern for thread safety and transaction isolation.
    
    Session Management:
        - Creates new session for each request
        - Automatic session cleanup with context manager
        - Thread-safe session isolation
        - Exception handling preserves database integrity
    
    Dependency Injection:
        - Used with FastAPI's Depends() system
        - Injected into endpoint functions automatically
        - Type hints provide IDE support and validation
        - Centralized session management
    
    Transaction Handling:
        - Sessions support database transactions
        - Rollback on exceptions (when using transactions)
        - Commit required for data persistence
        - Proper resource cleanup guaranteed
    
    Usage Pattern:
        ```python
        @app.post("/heroes/")
        def create_hero(hero: HeroCreate, session: SessionDep):
            # Session automatically provided and cleaned up
            db_hero = Hero.model_validate(hero)
            session.add(db_hero)
            session.commit()
            return db_hero
        ```
    
    Thread Safety:
        - Each request gets isolated session
        - No shared session state between requests
        - Concurrent request handling supported
        - Database connection pooling managed by engine
    
    Performance Considerations:
        - Session creation overhead per request
        - Connection pooling reduces connection costs
        - Session reuse within single request
        - Proper session cleanup prevents memory leaks
    
    Error Handling:
        - Session cleanup occurs even on exceptions
        - Database connections returned to pool
        - Transactions can be rolled back if needed
        - Resource leaks prevented by context manager
    
    Production Enhancements:
        - Add session-level logging
        - Implement connection health checks
        - Monitor session usage patterns
        - Add request correlation IDs
        - Implement automatic retry logic
    
    Alternative Patterns:
        ```python
        # With explicit transaction management
        @asynccontextmanager
        async def get_session_with_transaction():
            async with AsyncSession(engine) as session:
                async with session.begin():
                    yield session
        ```
    """
    with Session(engine) as session:
        yield session
        
# Type annotation for session dependency injection
SessionDep = Annotated[Session, Depends(get_session)]
"""
Type annotation for database session dependency injection.

This creates a reusable type alias that combines the Session type with
the dependency injection configuration, providing clean type hints
and centralized dependency management for all database operations.

Type Safety Benefits:
    - Clear type hints for IDE support
    - Automatic completion for session methods
    - Compile-time type checking
    - Self-documenting function signatures

Dependency Injection:
    - Annotated type combines Session with Depends()
    - Automatic session creation and cleanup
    - Consistent session management across endpoints
    - Centralized dependency configuration

Usage in Endpoints:
    ```python
    def create_hero(hero: HeroCreate, session: SessionDep):
        # session is automatically injected with proper type hints
        # IDE provides full autocompletion for session methods
    ```

Code Reusability:
    - Single definition used across all endpoints
    - Consistent dependency injection pattern
    - Easy to modify dependency configuration
    - Reduces code duplication

FastAPI Integration:
    - Compatible with OpenAPI documentation
    - Proper dependency graph construction
    - Exception handling by FastAPI framework
    - Automatic cleanup on request completion

Alternative Approaches:
    ```python
    # Direct usage (more verbose)
    def endpoint(session: Session = Depends(get_session)):
        pass
    
    # Multiple dependencies
    SessionDep = Annotated[Session, Depends(get_session)]
    UserDep = Annotated[User, Depends(get_current_user)]
    ```
"""

# Application lifespan management for database initialization
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context manager for application startup and shutdown.
    
    This function manages the application lifecycle, handling initialization
    tasks during startup and cleanup during shutdown. It replaces the
    deprecated @app.on_event pattern with the modern lifespan approach.
    
    Startup Operations:
        - Database table creation and schema initialization
        - Connection pool establishment
        - Cache warming and data preloading
        - External service connectivity checks
    
    Shutdown Operations:
        - Database connection cleanup
        - Background task termination
        - Resource deallocation
        - Graceful service disconnection
    
    Lifespan Pattern:
        - Modern FastAPI recommended approach
        - Replaces deprecated on_event decorators
        - Better error handling and resource management
        - Context manager ensures proper cleanup
    
    Database Initialization:
        - Creates all SQLModel tables if they don't exist
        - Ensures database schema matches model definitions
        - Safe for development (idempotent operations)
        - Production should use proper migrations
    
    Error Handling:
        - Startup failures prevent application launch
        - Database connection errors are propagated
        - Proper logging should be added for production
        - Graceful degradation strategies can be implemented
    
    Production Enhancements:
        ```python
        @asynccontextmanager
        async def lifespan(app: FastAPI):
            # Startup
            logger.info("Starting application...")
            try:
                # Database migrations
                run_database_migrations()
                
                # Health checks
                await verify_external_services()
                
                # Cache warming
                await warm_application_cache()
                
                logger.info("Application started successfully")
                yield
                
            except Exception as e:
                logger.error(f"Startup failed: {e}")
                raise
            finally:
                # Shutdown
                logger.info("Shutting down application...")
                await cleanup_resources()
                logger.info("Application shutdown complete")
        ```
    
    Development vs Production:
        - Development: Simple table creation
        - Production: Database migrations, health checks
        - Staging: Migration testing, service validation
        - Testing: In-memory database, mock services
    """
    # Startup: Create database tables
    create_db_and_tables()
    yield
    # Shutdown: Add any cleanup code here if needed

# FastAPI application instance with lifespan management
app = FastAPI(
    title="Hero Database API",
    description="SQLModel-powered superhero database with full CRUD operations",
    version="1.0.0",
    lifespan=lifespan
)

# Hero creation endpoint with input validation and response filtering
@app.post("/heroes/", response_model=HeroPublic)
def create_hero(hero: HeroCreate, session: SessionDep):
    """
    Create a new hero in the database.
    
    This endpoint accepts hero data, validates it, stores it in the database,
    and returns the created hero with public information only. It demonstrates
    the complete flow from request validation to database storage and response
    filtering for security.
    
    Args:
        hero (HeroCreate): Hero data including name, age, and secret_name
        session (SessionDep): Database session injected by FastAPI
    
    Returns:
        HeroPublic: Created hero with public fields only (excludes secret_name)
    
    Request Body:
        ```json
        {
            "name": "Spider-Man",
            "age": 25,
            "secret_name": "Peter Parker"
        }
        ```
    
    Response Body:
        ```json
        {
            "id": 1,
            "name": "Spider-Man",
            "age": 25
        }
        ```
    
    Database Operations:
        1. Validate input data using HeroCreate model
        2. Convert HeroCreate to Hero database model
        3. Add hero to database session
        4. Commit transaction to persist data
        5. Refresh object to get auto-generated ID
        6. Return hero data filtered through HeroPublic model
    
    SQLModel Conversion:
        - Hero.model_validate(hero): Converts HeroCreate → Hero
        - Automatic field mapping between compatible models
        - Type safety throughout conversion process
        - Pydantic validation ensures data integrity
    
    Security Features:
        - Input validation prevents malformed data
        - Response filtering excludes sensitive information
        - SQL injection prevention through ORM
        - Type validation for all fields
    
    Error Scenarios:
        - 422: Validation error (missing required fields, wrong types)
        - 500: Database connection or constraint errors
        - Field validation errors with detailed messages
    
    Usage Example:
        ```python
        import requests
        
        hero_data = {
            "name": "Wonder Woman",
            "age": 30,
            "secret_name": "Diana Prince"
        }
        
        response = requests.post(
            "http://localhost:8000/heroes/",
            json=hero_data
        )
        
        created_hero = response.json()
        print(f"Created hero with ID: {created_hero['id']}")
        ```
    
    Database Transaction:
        - session.add(): Adds object to session (not yet committed)
        - session.commit(): Persists changes to database
        - session.refresh(): Updates object with database-generated values
        - Automatic rollback on exceptions
    
    Production Considerations:
        - Add authentication and authorization
        - Implement rate limiting for creation endpoints
        - Add input sanitization for string fields
        - Include audit logging for hero creation
        - Consider duplicate detection logic
    """
    hero_db = Hero.model_validate(hero)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db  

# Heroes listing endpoint with pagination support
@app.get("/heroes/", response_model=list[HeroPublic])
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    """
    Retrieve a paginated list of heroes from the database.
    
    This endpoint returns heroes with pagination support to handle large
    datasets efficiently. It demonstrates query optimization, pagination
    patterns, and response filtering for public API consumption.
    
    Args:
        session (SessionDep): Database session injected by FastAPI
        offset (int): Number of records to skip (default: 0)
        limit (int): Maximum number of records to return (max: 100, default: 100)
    
    Returns:
        list[HeroPublic]: List of heroes with public information only
    
    Query Parameters:
        - offset: Starting position for pagination (e.g., ?offset=20)
        - limit: Number of results per page (e.g., ?limit=10)
    
    Response Format:
        ```json
        [
            {
                "id": 1,
                "name": "Spider-Man",
                "age": 25
            },
            {
                "id": 2,
                "name": "Wonder Woman",
                "age": 30
            }
        ]
        ```
    
    Pagination Implementation:
        - offset: Skip specified number of records
        - limit: Restrict maximum results (capped at 100)
        - Efficient database queries with LIMIT/OFFSET
        - Memory-efficient processing of large datasets
    
    Database Query:
        ```sql
        SELECT * FROM hero 
        ORDER BY id 
        LIMIT 100 OFFSET 0;
        ```
    
    Usage Examples:
        ```python
        # First page (default)
        response = requests.get("http://localhost:8000/heroes/")
        
        # Second page with custom limit
        response = requests.get("http://localhost:8000/heroes/?offset=10&limit=10")
        
        # Large page (up to limit)
        response = requests.get("http://localhost:8000/heroes/?limit=50")
        ```
    
    Query Optimization:
        - Database indexes on frequently queried fields
        - Efficient LIMIT/OFFSET implementation
        - Automatic response filtering through HeroPublic
        - Memory-efficient result processing
    
    Pagination Best Practices:
        - Limit maximum page size to prevent abuse
        - Consider cursor-based pagination for very large datasets
        - Include total count in headers (can be added)
        - Provide next/previous links in responses
    
    Performance Considerations:
        - Large offsets can be inefficient (use cursor pagination)
        - Index on ordering fields for better performance
        - Consider caching for frequently accessed pages
        - Monitor query execution times
    
    Enhanced Pagination Response:
        ```python
        # Production enhancement with metadata
        @app.get("/heroes/")
        def read_heroes_enhanced(session: SessionDep, offset: int = 0, limit: int = 100):
            heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
            total_count = session.exec(select(func.count(Hero.id))).one()
            
            return {
                "items": heroes,
                "total": total_count,
                "offset": offset,
                "limit": limit,
                "has_next": offset + limit < total_count
            }
        ```
    
    Security Considerations:
        - Rate limiting for list endpoints
        - Authentication for sensitive data access
        - Input validation for pagination parameters
        - Response size monitoring and limits
    """
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes

# Individual hero retrieval endpoint with error handling
@app.get("/heroes/{hero_id}", response_model=HeroPublic)
def read_hero(hero_id: int, session: SessionDep):
    """
    Retrieve a specific hero by their unique ID.
    
    This endpoint fetches a single hero from the database using their
    primary key ID. It demonstrates proper error handling for missing
    resources and response filtering for security.
    
    Args:
        hero_id (int): The unique identifier of the hero to retrieve
        session (SessionDep): Database session injected by FastAPI
    
    Returns:
        HeroPublic: Hero data with public information only
    
    Raises:
        HTTPException: 404 error if hero with specified ID doesn't exist
    
    Path Parameter:
        - hero_id: Integer ID in the URL path (e.g., /heroes/123)
    
    Response Format:
        ```json
        {
            "id": 1,
            "name": "Spider-Man",
            "age": 25
        }
        ```
    
    Database Operation:
        - session.get(Hero, hero_id): Efficient primary key lookup
        - Returns None if hero doesn't exist
        - Automatic conversion to HeroPublic response model
    
    Error Handling:
        - 404 Not Found: Hero with specified ID doesn't exist
        - 422 Unprocessable Entity: Invalid hero_id format
        - Proper HTTP status codes for different scenarios
    
    Usage Examples:
        ```python
        # Successful retrieval
        response = requests.get("http://localhost:8000/heroes/1")
        hero = response.json()
        
        # Hero not found (404)
        response = requests.get("http://localhost:8000/heroes/999")
        # Returns: {"detail": "Hero not found"}
        
        # Invalid ID format (422)
        response = requests.get("http://localhost:8000/heroes/abc")
        # FastAPI automatically handles validation error
        ```
    
    Security Features:
        - Response filtering excludes secret_name
        - Input validation for hero_id parameter
        - No sensitive information in error messages
        - SQL injection prevention through ORM
    
    Performance Optimization:
        - Primary key lookup is highly efficient
        - Database indexes ensure fast retrieval
        - Single query operation
        - Minimal memory usage
    
    Cache Integration:
        ```python
        # Production enhancement with caching
        @lru_cache(maxsize=128)
        def get_hero_cached(hero_id: int, session: SessionDep):
            hero = session.get(Hero, hero_id)
            if not hero:
                raise HTTPException(status_code=404, detail="Hero not found")
            return hero
        ```
    
    Alternative Error Handling:
        ```python
        # More detailed error responses
        hero = session.get(Hero, hero_id)
        if not hero:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "Hero not found",
                    "hero_id": hero_id,
                    "message": f"No hero exists with ID {hero_id}"
                }
            )
        ```
    
    Monitoring and Logging:
        - Log successful retrievals for analytics
        - Track 404 patterns for data insights
        - Monitor response times for performance
        - Alert on unusual access patterns
    """
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

# Hero update endpoint supporting partial updates via PATCH
@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_hero(hero_id: int, hero: HeroUpdate, session: SessionDep):
    """
    Update an existing hero with partial data using PATCH method.
    
    This endpoint allows partial updates of hero data, where clients
    can send only the fields they want to modify. It demonstrates
    proper PATCH semantics, data validation, and error handling.
    
    Args:
        hero_id (int): The unique identifier of the hero to update
        hero (HeroUpdate): Partial hero data with optional fields
        session (SessionDep): Database session injected by FastAPI
    
    Returns:
        HeroPublic: Updated hero data with public information only
    
    Raises:
        HTTPException: 404 error if hero with specified ID doesn't exist
    
    Request Body (Partial):
        ```json
        {
            "age": 26
        }
        ```
        
        ```json
        {
            "name": "Amazing Spider-Man",
            "secret_name": "Peter Benjamin Parker"
        }
        ```
    
    Response Format:
        ```json
        {
            "id": 1,
            "name": "Amazing Spider-Man",
            "age": 26
        }
        ```
    
    PATCH Semantics:
        - Only provided fields are updated
        - Omitted fields remain unchanged
        - exclude_unset=True filters out None values
        - Atomic update operation
    
    Update Process:
        1. Verify hero exists (404 if not found)
        2. Extract only provided fields from request
        3. Apply updates to database object
        4. Commit changes to database
        5. Refresh object with updated data
        6. Return filtered response
    
    Data Processing:
        ```python
        # hero.model_dump(exclude_unset=True) returns only non-None fields
        hero_data = {"age": 26}  # Only age was provided
        
        # hero_db.sqlmodel_update(hero_data) applies partial update
        hero_db.age = 26  # Only updates specified fields
        ```
    
    Usage Examples:
        ```python
        # Update only age
        response = requests.patch(
            "http://localhost:8000/heroes/1",
            json={"age": 26}
        )
        
        # Update multiple fields
        response = requests.patch(
            "http://localhost:8000/heroes/1",
            json={
                "name": "The Amazing Spider-Man",
                "secret_name": "Peter Benjamin Parker"
            }
        )
        
        # No changes (empty request body)
        response = requests.patch("http://localhost:8000/heroes/1", json={})
        ```
    
    Validation Features:
        - Type validation for all provided fields
        - Business logic validation (can be added)
        - Unchanged fields preserve existing data
        - Automatic JSON deserialization
    
    Error Scenarios:
        - 404: Hero not found
        - 422: Validation error in update data
        - 500: Database constraint violations
        - Field-specific validation errors
    
    Concurrency Considerations:
        ```python
        # Production enhancement with optimistic locking
        class Hero(HeroBase, table=True):
            version: int = Field(default=1)
            
        def update_hero_with_locking(hero_id: int, hero: HeroUpdate, session: SessionDep):
            hero_db = session.get(Hero, hero_id)
            if not hero_db:
                raise HTTPException(404, "Hero not found")
            
            # Check version for concurrent updates
            if hero.version != hero_db.version:
                raise HTTPException(409, "Resource was modified by another user")
            
            # Update with version increment
            hero_data = hero.model_dump(exclude_unset=True)
            hero_data["version"] = hero_db.version + 1
            hero_db.sqlmodel_update(hero_data)
        ```
    
    Audit Trail:
        ```python
        # Production enhancement with change tracking
        def update_hero_with_audit(hero_id: int, hero: HeroUpdate, session: SessionDep):
            hero_db = session.get(Hero, hero_id)
            old_values = hero_db.model_dump()
            
            # Apply updates
            hero_data = hero.model_dump(exclude_unset=True)
            hero_db.sqlmodel_update(hero_data)
            
            # Log changes
            audit_log = AuditLog(
                table_name="hero",
                record_id=hero_id,
                old_values=old_values,
                new_values=hero_db.model_dump(),
                changed_by=current_user.id
            )
            session.add(audit_log)
        ```
    
    Performance Optimization:
        - Single database transaction for atomicity
        - Efficient primary key lookup
        - Minimal data transfer (only changed fields)
        - Optimistic updates without locking
    """
    hero_db = session.get(Hero, hero_id)
    if not hero_db:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.model_dump(exclude_unset=True)
    hero_db.sqlmodel_update(hero_data)
    session.commit()
    session.refresh(hero_db)
    return hero_db

# Hero deletion endpoint with proper resource cleanup
@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    """
    Delete a hero from the database permanently.
    
    This endpoint removes a hero record from the database using their
    unique ID. It demonstrates proper resource deletion, error handling,
    and confirmation responses for DELETE operations.
    
    Args:
        hero_id (int): The unique identifier of the hero to delete
        session (SessionDep): Database session injected by FastAPI
    
    Returns:
        dict: Confirmation message indicating successful deletion
    
    Raises:
        HTTPException: 404 error if hero with specified ID doesn't exist
    
    Response Format:
        ```json
        {
            "ok": true
        }
        ```
    
    Deletion Process:
        1. Verify hero exists (404 if not found)
        2. Remove hero from database session
        3. Commit transaction to persist deletion
        4. Return confirmation response
    
    Database Operations:
        - session.get(Hero, hero_id): Locate hero by primary key
        - session.delete(hero_db): Mark object for deletion
        - session.commit(): Permanently remove from database
        - Cascade deletions handled automatically
    
    Usage Examples:
        ```python
        # Successful deletion
        response = requests.delete("http://localhost:8000/heroes/1")
        result = response.json()  # {"ok": true}
        
        # Hero not found (404)
        response = requests.delete("http://localhost:8000/heroes/999")
        # Returns: {"detail": "Hero not found"}
        ```
    
    Error Handling:
        - 404: Hero with specified ID doesn't exist
        - 422: Invalid hero_id format
        - 500: Database constraint violations
        - Foreign key constraint errors (if relationships exist)
    
    Security Considerations:
        - Verify user permissions before deletion
        - Audit log deletion operations
        - Prevent accidental bulk deletions
        - Confirm critical resource deletions
    
    Soft Delete Alternative:
        ```python
        # Production pattern: soft delete instead of hard delete
        class Hero(HeroBase, table=True):
            deleted_at: datetime | None = Field(default=None)
            
        def soft_delete_hero(hero_id: int, session: SessionDep):
            hero_db = session.get(Hero, hero_id)
            if not hero_db:
                raise HTTPException(404, "Hero not found")
            
            hero_db.deleted_at = datetime.utcnow()
            session.commit()
            return {"ok": True}
        ```
    
    Cascade Deletion:
        ```python
        # Handle related records
        def delete_hero_with_relationships(hero_id: int, session: SessionDep):
            hero_db = session.get(Hero, hero_id)
            if not hero_db:
                raise HTTPException(404, "Hero not found")
            
            # Delete related records first
            session.exec(delete(Mission).where(Mission.hero_id == hero_id))
            session.exec(delete(Equipment).where(Equipment.hero_id == hero_id))
            
            # Delete hero
            session.delete(hero_db)
            session.commit()
        ```
    
    Confirmation Pattern:
        ```python
        # Enhanced deletion with confirmation
        @app.delete("/heroes/{hero_id}")
        def delete_hero_confirmed(
            hero_id: int, 
            confirm: bool = Query(False),
            session: SessionDep
        ):
            if not confirm:
                return {
                    "message": "Deletion requires confirmation",
                    "confirm_url": f"/heroes/{hero_id}?confirm=true"
                }
            
            # Proceed with deletion
            hero_db = session.get(Hero, hero_id)
            if not hero_db:
                raise HTTPException(404, "Hero not found")
            
            session.delete(hero_db)
            session.commit()
            return {"ok": True, "deleted_hero_id": hero_id}
        ```
    
    Audit and Logging:
        ```python
        # Production enhancement with audit trail
        def delete_hero_with_audit(hero_id: int, session: SessionDep, current_user: User):
            hero_db = session.get(Hero, hero_id)
            if not hero_db:
                raise HTTPException(404, "Hero not found")
            
            # Log deletion
            audit_log = AuditLog(
                action="DELETE",
                table_name="hero",
                record_id=hero_id,
                old_values=hero_db.model_dump(),
                deleted_by=current_user.id,
                deleted_at=datetime.utcnow()
            )
            session.add(audit_log)
            
            # Delete hero
            session.delete(hero_db)
            session.commit()
        ```
    
    Performance Considerations:
        - Primary key lookups are highly efficient
        - Single transaction for atomicity
        - Cascade deletions may impact performance
        - Consider batch deletion for multiple records
    
    Recovery Options:
        - Database backups for recovery
        - Soft delete for easy restoration
        - Audit trails for reconstruction
        - Version control for critical data
    """
    hero_db = session.get(Hero, hero_id)
    if not hero_db:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero_db)
    session.commit()
    return {"ok": True}