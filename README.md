# FastAPI Hands-On Review

A comprehensive review and practice of the FastAPI framework.

## Lesson 1: First FastAPI Service

### Overview
- Simple "Hello World" application
- Basic FastAPI service setup and execution

### Running the Application
```bash
fastapi dev main.py
```

### Installing Dependencies
1. Install pipreqs to generate requirements:
   ```bash
   pip install pipreqs
   ```

2. Generate requirements.txt:
   ```bash
   pipreqs /path/to/project
   ```

### Git Management
To remove the virtual environment from git tracking:
```bash
git rm -r --cached venv/
```

### Project Structure
```
FastAPI_handson/
├── main.py
├── path_parameters.py
├── query_parameters.py
├── request_body.py
├── query_param_and_string_val.py
├── path_validations.py
├── 7bodymultipleparameters.py
├── 8body_fields.py
├── 9bodynetedmodels.py
├── 10extradatatypes.py
├── 11responsemodelreturntype.py
├── README.md
├── requirements.txt
├── .gitignore
└── __pycache__/
```

## Lesson 2: Path Parameters

### Overview
- Understanding path parameters in FastAPI
- Type validation and conversion
- Route ordering and precedence
- Practical examples with different data types

### File: `path_parameters.py`

This lesson demonstrates how to capture and use path parameters in FastAPI endpoints.

## Lesson 11: Response Models and Return Types

### Overview
- Response model declaration using return type annotations
- Combining response_model parameter with return type annotations
- Automatic JSON serialization based on response models
- Returning Pydantic models and lists of models
- API documentation generation from response models
- Data validation and filtering for API responses

### File: `11responsemodelreturntype.py`

This lesson demonstrates how to declare response models using return type annotations and the response_model parameter in FastAPI, enabling automatic validation, serialization, and API documentation generation for your endpoint responses.

### Key Concepts Covered
1. **Return Type Annotations**: Using `-> Type` syntax to declare response structure
2. **response_model Parameter**: Explicit response model declaration
3. **Pydantic Model Responses**: Returning structured data with validation
4. **List Response Models**: Returning arrays of validated objects
5. **Automatic Serialization**: JSON conversion based on model structure
6. **API Documentation**: Enhanced OpenAPI docs from response models

### Running the Application
```bash
fastapi dev 11responsemodelreturntype.py
```

### Pydantic Model
```python
class Item(BaseModel):
    name: str                           # Required item name
    description: str | None = None      # Optional description
    price: float                        # Required price (float)
    tax: float | None = None           # Optional tax amount
    tags: list[str] = []               # Optional list of tags (defaults to empty)
```

### Endpoints

#### 1. Single Model Response (`POST /items/`)
- **Purpose**: Create and return a single item
- **Response Model**: Item (declared with `response_model=Item`)
- **Return Type**: `-> Item` (type annotation)
- **Behavior**: Returns the exact item data sent in request

#### 2. List of Models Response (`GET /items/`)
- **Purpose**: Retrieve a list of items
- **Response Model**: `list[Item]` (declared with `response_model=list[Item]`)
- **Return Type**: `-> list[Item]` (type annotation)
- **Behavior**: Returns array of sample items with automatic field completion

### Example Usage

#### Create Item (Single Response)
```bash
curl -X POST "http://localhost:8000/items/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "description": "Gaming laptop",
    "price": 999.99,
    "tax": 99.99,
    "tags": ["electronics", "gaming"]
  }'
```

#### Response
```json
{
  "name": "Laptop",
  "description": "Gaming laptop",
  "price": 999.99,
  "tax": 99.99,
  "tags": ["electronics", "gaming"]
}
```

#### Get Items (List Response)
```bash
curl -X GET "http://localhost:8000/items/"
```

#### Response
```json
[
  {
    "name": "Portal Gun",
    "description": null,
    "price": 42.0,
    "tax": null,
    "tags": []
  },
  {
    "name": "Plumbus",
    "description": null,
    "price": 32.0,
    "tax": null,
    "tags": []
  }
]
```

### Response Model Features

#### Automatic Field Completion
The sample data in `read_items()` only includes `name` and `price`:
```python
return [
    {"name": "Portal Gun", "price": 42.0},
    {"name": "Plumbus", "price": 32.0},
]
```

FastAPI automatically adds missing optional fields based on the Item model:
- `description: null` (default for optional fields)
- `tax: null` (default for optional fields)
- `tags: []` (default empty list)

#### Response Model Benefits
| Feature | Description | Example |
|---------|-------------|---------|
| **Type Safety** | Return type validation | Prevents returning wrong data structure |
| **Auto-completion** | Missing fields get defaults | `null` for optional, `[]` for lists |
| **Documentation** | OpenAPI schema generation | Swagger UI shows exact response format |
| **Serialization** | Automatic JSON conversion | Python objects → JSON responses |

### Return Type Annotation vs response_model

#### Both Used Together (Recommended)
```python
@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Item:
    return item
```

**Benefits:**
- **Editor Support**: IDEs understand return type for autocomplete
- **Runtime Validation**: FastAPI validates response matches model
- **Documentation**: OpenAPI docs show response structure
- **Type Checking**: Static analysis tools can verify code

#### response_model Only
```python
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item
```

**Missing:** Editor type hints and static analysis benefits

#### Return Type Only
```python
@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item
```

**Missing:** Runtime response validation and filtering

### Advanced Response Model Patterns

#### Partial Data Handling
```python
# Function returns partial data
def get_item_summary():
    return {"name": "Item", "price": 99.99}
    # Missing: description, tax, tags

# FastAPI completes the response:
{
    "name": "Item",
    "price": 99.99,
    "description": null,
    "tax": null,
    "tags": []
}
```

#### List Response Validation
```python
@app.get("/items/", response_model=list[Item])
async def read_items() -> list[Item]:
    # Each item in the list is validated against Item model
    return [
        {"name": "Item 1", "price": 10.0},
        {"name": "Item 2", "price": 20.0, "description": "Has description"},
    ]
```

### Response Model Use Cases

#### E-commerce APIs
```python
# Product listings with consistent structure
@app.get("/products/", response_model=list[Product])
async def list_products() -> list[Product]:
    products = database.get_products()  # May have varying fields
    return products  # FastAPI ensures consistent response structure
```

#### User Management
```python
# User profile with sensitive data filtering
@app.get("/users/me", response_model=UserProfile)
async def get_current_user(user: User = Depends(get_current_user)) -> UserProfile:
    return user  # Only UserProfile fields are returned, sensitive data filtered
```

#### API Data Transformation
```python
# Database model → API response model
@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int) -> ItemResponse:
    db_item = database.get_item(item_id)  # Database model
    return ItemResponse.from_orm(db_item)  # Convert to API response model
```

### Error Handling and Validation

#### Response Validation Errors
If your function returns data that doesn't match the response model, FastAPI raises an error:

```python
@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Item:
    return {"invalid": "structure"}  # ❌ Doesn't match Item model
    # Results in: Internal Server Error
```

#### Proper Error Handling
```python
@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Item:
    try:
        # Process item
        return item  # ✓ Matches Item model
    except Exception:
        raise HTTPException(status_code=500, detail="Item creation failed")
```

### OpenAPI Documentation Benefits

#### Automatic Schema Generation
Response models automatically generate:
- **Response examples** in Swagger UI
- **JSON Schema** for response structure
- **Field descriptions** from model docstrings
- **Type information** for all fields
- **Required vs optional** field indicators

#### API Client Generation
Response models enable:
- **TypeScript interfaces** for frontend clients
- **Python client libraries** with proper typing
- **Code generation tools** for various languages
- **API testing tools** with schema validation

### Key Learning Points
- **Response models ensure consistent API responses** regardless of data source
- **Return type annotations provide excellent developer experience** with editor support
- **Combining both approaches gives maximum benefits** for development and runtime
- **FastAPI automatically completes missing optional fields** based on model defaults
- **Response validation prevents accidentally exposing** incorrect data structures
- **OpenAPI documentation quality improves significantly** with proper response models
- **Type safety extends to API responses** enabling better client-side development
- **Response models work seamlessly with lists** and complex nested structures

This lesson establishes the foundation for building type-safe, well-documented APIs with predictable response structures that improve both developer experience and API reliability!

### Key Concepts Covered
1. **Basic Path Parameters**: Capturing URL segments as variables
2. **Type Hints**: Automatic validation and conversion of path parameters
3. **Route Ordering**: Understanding how FastAPI matches routes
4. **Error Handling**: Validation errors for invalid parameter types

### Running the Application
```bash
fastapi dev path_parameters.py
```

### Endpoints
- `GET /items/{item_id}` - Basic string path parameter
- `GET /items/{item_id}/typed` - Integer path parameter with validation
- `GET /users/me` - Fixed path (demonstrates route precedence)
- `GET /users/{user_id}` - User-specific path parameter

### Example Usage
```bash
# String parameter
curl http://localhost:8000/items/foo

# Integer parameter (valid)
curl http://localhost:8000/items/123/typed

# Integer parameter (invalid - returns 422)
curl http://localhost:8000/items/abc/typed

# Fixed route
curl http://localhost:8000/users/me

# Dynamic user route
curl http://localhost:8000/users/john
```

## Lesson 3: Query Parameters

### Overview
- Understanding query parameters in FastAPI
- Default values and optional parameters
- Combining path and query parameters
- Type validation for query parameters
- URL encoding and parameter parsing

### File: `query_parameters.py`

This lesson demonstrates how to use query parameters in FastAPI endpoints for filtering, pagination, and optional functionality.

### Key Concepts Covered
1. **Basic Query Parameters**: Using optional parameters with default values
2. **Parameter Combination**: Mixing path and query parameters in one endpoint
3. **Type Validation**: Automatic conversion and validation of query parameter types
4. **Optional Parameters**: Using `Union[str, None]` for optional string parameters
5. **URL Encoding**: How FastAPI handles special characters in URLs

### Running the Application
```bash
fastapi dev query_parameters.py
```

### Endpoints
- `GET /items/` - Pagination with skip and limit query parameters
- `GET /items/{item_id}` - Item retrieval with optional search query

### Example Usage
```bash
# Basic pagination (uses defaults)
curl http://localhost:8000/items/

# Custom pagination parameters
curl http://localhost:8000/items/?skip=5&limit=20

# Single parameter
curl http://localhost:8000/items/?skip=10

# Item with optional query
curl http://localhost:8000/items/42

# Item with search query
curl http://localhost:8000/items/42?q=search

# Query with spaces (URL encoded)
curl "http://localhost:8000/items/42?q=hello%20world"

# Invalid item_id (returns 422)
curl http://localhost:8000/items/abc?q=test
```

### Query Parameter Features
- **Default Values**: Parameters have sensible defaults when not provided
- **Type Safety**: Automatic validation and conversion (int, str, bool, etc.)
- **Optional Parameters**: Can be omitted entirely from the request
- **Multiple Parameters**: Combine multiple query parameters with `&`
- **URL Encoding**: Special characters are automatically decoded

## Lesson 4: Request Bodies

### Overview
- Understanding request bodies in FastAPI
- Pydantic models for data validation
- POST and PUT operations with structured data
- Combining path parameters with request bodies
- Dictionary unpacking with model_dump()

### File: `request_body.py`

This lesson demonstrates how to handle structured data sent in request bodies using Pydantic models for automatic validation and serialization.

### Key Concepts Covered
1. **Pydantic Models**: Using BaseModel for data structure and validation
2. **Request Body Handling**: Receiving JSON data in POST/PUT requests
3. **Type Validation**: Automatic validation of complex data structures
4. **Optional Fields**: Using Union types with default values
5. **Model Serialization**: Converting models to dictionaries with model_dump()
6. **Dictionary Unpacking**: Using ** operator to merge data structures

### Running the Application
```bash
fastapi dev request_body.py
```

### Endpoints
- `POST /items/` - Create a new item with request body validation
- `PUT /items/{item_id}` - Update an item combining path parameter and request body

### Data Model
```json
{
    "name": "string (required)",
    "description": "string or null (optional)",
    "price": "float (required)",
    "tax": "float or null (optional)"
}
```

### Example Usage
```bash
# Create item with all fields
curl -X POST "http://localhost:8000/items/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "description": "Gaming laptop",
    "price": 999.99,
    "tax": 99.99
  }'

# Create item with only required fields
curl -X POST "http://localhost:8000/items/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mouse",
    "price": 29.99
  }'

# Update item (combines path param + body)
curl -X PUT "http://localhost:8000/items/123" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Laptop",
    "description": "High-end gaming laptop",
    "price": 1299.99,
    "tax": 129.99
  }'

# Invalid request (missing required field)
curl -X POST "http://localhost:8000/items/" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "No name provided"
  }'
```

### Request Body Features
- **Automatic Validation**: Pydantic validates data types and required fields
- **JSON Parsing**: FastAPI automatically parses JSON request bodies
- **Error Messages**: Detailed validation errors for invalid data (422 status)
- **Optional Fields**: Fields can be omitted and will use default values
- **Type Conversion**: Automatic conversion between compatible types
- **Model Serialization**: Easy conversion from models to dictionaries

## Lesson 5: Query Parameter Validation and String Validation

### Overview
- Advanced query parameter validation using Query class
- String length constraints and validation rules
- Numeric parameter constraints (min/max values)
- Required vs optional parameters with custom validation
- Search functionality with list comprehensions
- Parameter descriptions for auto-generated API documentation

### File: `query_param_and_string_val.py`

This lesson demonstrates advanced query parameter validation techniques using FastAPI's Query class for robust input validation and search functionality.

### Key Concepts Covered
1. **Query Class**: Using `Query()` for advanced parameter validation
2. **String Constraints**: Setting min_length and max_length for string parameters
3. **Numeric Constraints**: Using ge (>=) and le (<=) for numeric validation
4. **Required Parameters**: Making query parameters mandatory
5. **Parameter Descriptions**: Adding documentation for auto-generated API docs
6. **List Comprehensions**: Efficient data filtering and search implementation
7. **Case-insensitive Search**: Practical search functionality

### Running the Application
```bash
fastapi dev query_param_and_string_val.py
```

### Endpoints
- `GET /items/` - Basic search with optional query parameter (max 50 chars)
- `GET /items/search/` - Advanced search with required query (3-50 chars) and result limiting

### Sample Data
```json
[
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"}
]
```

### Example Usage
```bash
# Basic search - optional query
curl http://localhost:8000/items/
curl http://localhost:8000/items/?q=foo
curl http://localhost:8000/items/?q=ba

# Advanced search - required query with constraints
curl http://localhost:8000/items/search/?q=foo
curl http://localhost:8000/items/search/?q=bar&limit=1

# Validation errors
curl http://localhost:8000/items/?q=verylongquerystringthatexceedsfiftycharacterslimit  # 422 Error
curl http://localhost:8000/items/search/?q=ab  # 422 Error (too short)
curl http://localhost:8000/items/search/?q=foo&limit=0  # 422 Error (below minimum)
curl http://localhost:8000/items/search/?q=foo&limit=150  # 422 Error (above maximum)
curl http://localhost:8000/items/search/  # 422 Error (missing required parameter)
```

### Query Parameter Validation Features

#### Basic Search (`/items/`):
- **q parameter**: Optional string with max_length=50
- **Default behavior**: Returns empty array if no query provided
- **Validation**: 422 error if query exceeds 50 characters

#### Advanced Search (`/items/search/`):
- **q parameter**: Required string with min_length=3, max_length=50
- **limit parameter**: Integer with ge=1, le=100, default=10
- **Descriptions**: Both parameters have documentation descriptions
- **Strict validation**: More robust input checking

### Search Implementation Features
- **Case-insensitive matching**: Search works with any case combination
- **Partial matching**: Finds items containing the search string (substring search)
- **List comprehensions**: Efficient filtering using Python list comprehensions
- **Result limiting**: Pagination support with configurable limits
- **Empty result handling**: Graceful handling of no matches found

### Validation Constraints Summary
| Parameter | Type | Min Length | Max Length | Min Value | Max Value | Required | Default |
|-----------|------|------------|------------|-----------|-----------|----------|---------|
| q (basic) | str  | -          | 50         | -         | -         | No       | None    |
| q (search)| str  | 3          | 50         | -         | -         | Yes      | -       |
| limit     | int  | -          | -          | 1         | 100       | No       | 10      |

## Lesson 6: Path Parameter Validation

### Overview
- Advanced path parameter validation using Path class
- Numeric constraints for path parameters (ge, le)
- Combining path and query parameter validations
- Adding metadata and descriptions to path parameters
- Understanding parameter order and precedence

### File: `path_validations.py`

This lesson demonstrates how to add validation constraints and metadata to path parameters using FastAPI's Path class for robust URL parameter validation.

### Key Concepts Covered
1. **Path Class**: Using `Path()` for advanced path parameter validation
2. **Numeric Constraints**: Setting ge (>=) and le (<=) for numeric path parameters
3. **Parameter Metadata**: Adding title and description for documentation
4. **Combined Validation**: Using both Path and Query validations together
5. **Parameter Order**: Understanding how FastAPI evaluates parameters
6. **API Documentation**: How metadata improves auto-generated docs

### Running the Application
```bash
fastapi dev path_validations.py
```

### Endpoints
- `GET /items/{item_id}` - Basic path parameter with ge=1 constraint
- `GET /items/{item_id}/details` - Combined path (1-1000) and query validation
- `GET /users/{user_id}` - Path parameter with title and description metadata

### Example Usage
```bash
# Basic path validation - item_id must be >= 1
curl http://localhost:8000/items/1
curl http://localhost:8000/items/999

# Combined path and query validation
curl http://localhost:8000/items/500/details
curl http://localhost:8000/items/500/details?q=search

# User endpoint with metadata
curl http://localhost:8000/users/123

# Validation errors
curl http://localhost:8000/items/0           # 422 Error (item_id < 1)
curl http://localhost:8000/items/-5          # 422 Error (negative number)
curl http://localhost:8000/items/1001/details # 422 Error (item_id > 1000)
curl http://localhost:8000/users/0           # 422 Error (user_id < 1)
```

### Path Parameter Validation Features

#### Basic Path Validation (`/items/{item_id}`):
- **item_id**: Integer with ge=1 (must be >= 1)
- **Error handling**: 422 validation error for invalid values
- **Simple constraint**: Demonstrates basic numeric validation

#### Combined Validation (`/items/{item_id}/details`):
- **item_id**: Integer with ge=1, le=1000 (range 1-1000)
- **q**: Optional query string with max_length=50
- **Description**: Path parameter includes documentation description
- **Multiple constraints**: Shows how to combine different validation types

#### Metadata Example (`/users/{user_id}`):
- **user_id**: Integer with ge=1
- **title**: "User ID" for documentation
- **description**: Detailed explanation of the parameter
- **Documentation**: Enhances auto-generated API docs

### Path Validation Constraints
| Endpoint | Parameter | Type | Min Value | Max Value | Required | Metadata |
|----------|-----------|------|-----------|-----------|----------|----------|
| `/items/{item_id}` | item_id | int | 1 | - | Yes | None |
| `/items/{item_id}/details` | item_id | int | 1 | 1000 | Yes | Description |
| `/users/{user_id}` | user_id | int | 1 | - | Yes | Title + Description |

### Key Learning Points
- **Path parameters are always required** (unlike query parameters)
- **Validation happens before the function executes**
- **Invalid path parameters return 422 Validation Error**
- **Metadata improves API documentation quality**
- **ge/le constraints work with any numeric type**
- **Path evaluation occurs before query parameter processing**
- **Combining Path and Query validations provides comprehensive input validation**

## Lesson 7: Multiple Body Parameters

### Overview
- Advanced request body handling with multiple Pydantic models
- Mixing path, query, and body parameters in complex scenarios
- Singular values in request body using Body()
- Multiple body parameters with validation constraints
- Body embedding techniques for consistent JSON structure

### File: `7bodymultipleparameters.py`

This lesson demonstrates the most advanced FastAPI request handling techniques, showing how to combine multiple body parameters, path parameters, and query parameters in sophisticated ways.

### Key Concepts Covered
1. **Mixed Parameter Types**: Combining path, query, and body parameters
2. **Multiple Body Parameters**: Using multiple Pydantic models in one endpoint
3. **Singular Body Values**: Including scalar values in request body with Body()
4. **Complex Validation**: Multiple body parameters with constraints and queries
5. **Body Embedding**: Using Body(embed=True) for consistent JSON structure

### Running the Application
```bash
fastapi dev 7bodymultipleparameters.py
```

### Pydantic Models
```python
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

class User(BaseModel):
    username: str
    full_name: Union[str, None] = None
```

### Endpoints

#### 1. Mixed Parameters (`PUT /items/{item_id}/basic`)
- **Path**: item_id (0-1000) with validation
- **Query**: q (optional string)
- **Body**: item (optional Item model)

#### 2. Multiple Body Parameters (`PUT /items/{item_id}`)
- **Path**: item_id
- **Body**: Both Item and User models

#### 3. Singular Body Values (`PUT /items/{item_id}/importance`)
- **Path**: item_id
- **Body**: Item model, User model, and importance (integer)

#### 4. Full Parameter Mix (`PUT /items/{item_id}/full`)
- **Path**: item_id
- **Body**: Item, User, importance (>0 validation)
- **Query**: q (optional)

#### 5. Embedded Body (`PUT /items/{item_id}/embed`)
- **Path**: item_id
- **Body**: Item model with embed=True

### Example Usage

#### Mixed Parameters
```bash
curl -X PUT "http://localhost:8000/items/123/basic?q=search" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "price": 999.99
  }'
```

#### Multiple Body Parameters
```bash
curl -X PUT "http://localhost:8000/items/456" \
  -H "Content-Type: application/json" \
  -d '{
    "item": {
      "name": "Gaming Mouse",
      "price": 59.99,
      "tax": 5.99
    },
    "user": {
      "username": "john_doe",
      "full_name": "John Doe"
    }
  }'
```

#### Singular Body Values
```bash
curl -X PUT "http://localhost:8000/items/789/importance" \
  -H "Content-Type: application/json" \
  -d '{
    "item": {
      "name": "Mechanical Keyboard",
      "price": 149.99
    },
    "user": {
      "username": "jane_smith"
    },
    "importance": 8
  }'
```

#### Full Parameter Mix with Validation
```bash
curl -X PUT "http://localhost:8000/items/999/full?q=urgent" \
  -H "Content-Type: application/json" \
  -d '{
    "item": {
      "name": "Monitor",
      "description": "4K Gaming Monitor",
      "price": 399.99,
      "tax": 40.00
    },
    "user": {
      "username": "admin",
      "full_name": "System Administrator"
    },
    "importance": 10
  }'
```

#### Embedded Body
```bash
curl -X PUT "http://localhost:8000/items/111/embed" \
  -H "Content-Type: application/json" \
  -d '{
    "item": {
      "name": "Wireless Headphones",
      "description": "Noise-cancelling headphones",
      "price": 199.99,
      "tax": 20.00
    }
  }'
```

### Request Body Structure Variations

| Endpoint | Structure | Key Feature |
|----------|-----------|-------------|
| `/basic` | Optional root-level item | Mixed optional parameters |
| Base endpoint | `{"item": {...}, "user": {...}}` | Multiple body models |
| `/importance` | `{"item": {...}, "user": {...}, "importance": 8}` | Scalar in body |
| `/full` | Same as importance + query param | Full parameter mix |
| `/embed` | `{"item": {...}}` | Single model embedded |

### Advanced Features Demonstrated

#### Union Types for Optional Fields
- **`Union[str, None]`**: Fields that can be string or null
- **Default values**: Using `= None` for optional fields
- **Flexible APIs**: Supporting partial data updates

#### Body() Function Usage
- **Scalar values**: Including simple types in request body
- **Validation**: Adding constraints like `Body(gt=0)`
- **Embedding**: Using `Body(embed=True)` for structure consistency

#### Parameter Mixing Best Practices
- **Order independence**: FastAPI handles parameter detection automatically
- **Type safety**: Full validation across all parameter types
- **Documentation**: Auto-generated docs show complete request structure

### Validation and Error Handling
- **422 Validation Errors**: For invalid data types or constraint violations
- **Required fields**: Missing required fields in models
- **Constraint validation**: Body(gt=0) and other constraints
- **Type conversion**: Automatic conversion where possible

This lesson represents the most sophisticated request handling in FastAPI, combining all parameter types with advanced validation and flexible JSON structures!

## Lesson 8: Body Fields Validation

### Overview
- Advanced Pydantic field validation using Field() function
- Adding validation constraints and metadata to model attributes
- Numeric constraints (gt, ge, lt, le) for number fields
- String constraints (max_length, min_length) for text fields
- Field metadata for enhanced API documentation
- Combining Field validation with Body embedding

### File: `8body_fields.py`

This lesson demonstrates how to add fine-grained validation and documentation to individual fields within Pydantic models using the Field() function for precise data validation control.

### Key Concepts Covered
1. **Pydantic Field() Function**: Advanced field-level validation and metadata
2. **Numeric Constraints**: Using gt, ge, lt, le for number validation
3. **String Constraints**: Setting max_length, min_length for text fields
4. **Field Metadata**: Adding title and description for documentation
5. **Validation Integration**: How Field validation works with FastAPI
6. **Body Embedding**: Combining Field validation with Body(embed=True)

### Running the Application
```bash
fastapi dev 8body_fields.py
```

### Pydantic Model with Field Validation
```python
class Item(BaseModel):
    name: str  # Simple required field
    description: Union[str, None] = Field(
        default=None, 
        title="The description of the item", 
        max_length=300
    )
    price: float = Field(
        gt=0, 
        description="The price must be greater than zero"
    )
    tax: Union[float, None] = None  # Optional, no validation
```

### Endpoint
- `PUT /items/{item_id}` - Update item with Field-validated request body

### Field Validation Features

#### Field Constraints
| Field | Type | Constraints | Metadata | Purpose |
|-------|------|-------------|----------|---------|
| name | str | None | None | Simple required field |
| description | str\|None | max_length=300 | Custom title | Optional with length limit |
| price | float | gt=0 | Custom description | Required positive number |
| tax | float\|None | None | None | Optional, no validation |

#### Validation Types
- **gt=0**: Greater than zero (price must be positive)
- **max_length=300**: Maximum string length (description limit)
- **default=None**: Default value for optional fields
- **title/description**: Metadata for API documentation

### Example Usage

#### Valid Request
```bash
curl -X PUT "http://localhost:8000/items/123" \
  -H "Content-Type: application/json" \
  -d '{
    "item": {
      "name": "Gaming Laptop",
      "description": "High-end gaming laptop with RTX graphics",
      "price": 1299.99,
      "tax": 130.00
    }
  }'
```

#### Response
```json
{
  "item_id": 123,
  "item": {
    "name": "Gaming Laptop",
    "description": "High-end gaming laptop with RTX graphics",
    "price": 1299.99,
    "tax": 130.0
  }
}
```

#### Validation Error Examples
```bash
# Price <= 0 (violates gt=0)
curl -X PUT "http://localhost:8000/items/123" \
  -H "Content-Type: application/json" \
  -d '{
    "item": {
      "name": "Free Item",
      "price": 0
    }
  }'
# Returns: 422 "ensure this value is greater than 0"

# Description too long (violates max_length=300)
curl -X PUT "http://localhost:8000/items/123" \
  -H "Content-Type: application/json" \
  -d '{
    "item": {
      "name": "Item",
      "description": "Very long description that exceeds 300 characters...",
      "price": 99.99
    }
  }'
# Returns: 422 "ensure this value has at most 300 characters"

# Missing required fields
curl -X PUT "http://localhost:8000/items/123" \
  -H "Content-Type: application/json" \
  -d '{
    "item": {
      "description": "Missing name and price"
    }
  }'
# Returns: 422 "field required" for name and price
```

### Field Validation Benefits

#### Data Integrity
- **Automatic validation**: Before function execution
- **Type safety**: Ensures correct data types
- **Constraint enforcement**: Business rule validation
- **Consistent validation**: Across all endpoints using the model

#### API Documentation Enhancement
- **Field metadata**: Custom titles and descriptions appear in docs
- **Constraint visibility**: Validation rules shown in API documentation
- **Example generation**: Better examples in auto-generated docs
- **User guidance**: Clear field requirements and limitations

#### Error Handling
- **Detailed error messages**: Specific validation failure reasons
- **422 status codes**: Standard validation error responses
- **Field-level errors**: Pinpoint which fields failed validation
- **User-friendly feedback**: Clear guidance on how to fix errors

### Common Field Validation Patterns

#### Numeric Constraints
```python
price: float = Field(gt=0)              # Greater than 0
quantity: int = Field(ge=1, le=100)     # Between 1 and 100
rating: float = Field(ge=0.0, le=5.0)   # Rating scale 0-5
```

#### String Constraints
```python
name: str = Field(min_length=1, max_length=100)
email: str = Field(regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
description: str = Field(max_length=500)
```

#### Optional Fields with Metadata
```python
bio: Union[str, None] = Field(
    default=None,
    title="User Biography",
    description="Optional user biography",
    max_length=1000
)
```

### Key Learning Points
- **Field() provides granular control** over individual model attributes
- **Validation happens automatically** during request processing
- **Metadata enhances API documentation** quality significantly
- **Constraint violations return detailed 422 errors** with specific messages
- **Field validation is reusable** across multiple endpoints using the same model
- **Combines perfectly with Body embedding** for consistent JSON structure
- **Supports all standard validation patterns** needed in real-world APIs

## Lesson 9: Body Nested Models

### Overview
- Complex nested data structures with Pydantic models
- Models within models for hierarchical data
- Collections of nested models (lists, sets, dictionaries)
- HttpUrl validation for URL fields
- Real-world patterns for sophisticated API design
- Handling complex relationships between data entities

### File: `9bodynetedmodels.py`

This lesson demonstrates how to create and handle complex nested data structures using Pydantic models, enabling sophisticated API designs that mirror real-world data relationships.

### Key Concepts Covered
1. **Nested Models**: Models containing other models as fields
2. **Collections of Models**: Lists and sets of nested models
3. **Dictionary Types**: Key-value mappings with type constraints
4. **URL Validation**: HttpUrl type for proper URL validation
5. **Complex Validation**: Nested validation throughout the hierarchy
6. **Real-World Patterns**: Product catalogs, image galleries, configuration data

### Running the Application
```bash
fastapi dev 9bodynetedmodels.py
```

### Pydantic Models Structure

#### Image Model (Nested Component)
```python
class Image(BaseModel):
    url: HttpUrl      # Validated URL format
    name: str         # Image display name
```

#### Item Model (Single Nested)
```python
class Item(BaseModel):
    name: str                           # Required item name
    description: Union[str, None] = None # Optional description
    price: float                        # Required price
    tax: Union[float, None] = None      # Optional tax
    tags: Set[str] = set()             # Unique tags (no duplicates)
    image: Union[Image, None] = None    # Optional single image
```

#### ItemWithImages Model (List of Nested)
```python
class ItemWithImages(BaseModel):
    name: str                           # Required item name
    description: Union[str, None] = None # Optional description
    price: float                        # Required price
    tax: Union[float, None] = None      # Optional tax
    tags: Set[str] = set()             # Unique tags
    images: List[Image] = []            # List of images (can be empty)
```

### Endpoints

#### 1. Single Nested Model (`PUT /items/{item_id}`)
- **Purpose**: Handle item with optional single image
- **Model**: Item with optional Image nested model
- **Use Case**: Products with primary image

#### 2. List of Nested Models (`PUT /items/{item_id}/images`)
- **Purpose**: Handle item with multiple images
- **Model**: ItemWithImages with list of Image models
- **Use Case**: Product galleries, multi-image documentation

#### 3. Dictionary Types (`POST /index-weights/`)
- **Purpose**: Handle key-value mappings
- **Type**: Dict[int, float] for index weights
- **Use Case**: Rankings, priorities, configuration values

### Example Usage

#### Single Nested Model
```bash
curl -X PUT "http://localhost:8000/items/123" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Gaming Laptop",
    "description": "High-performance gaming laptop with RTX graphics",
    "price": 1299.99,
    "tax": 130.00,
    "tags": ["gaming", "laptop", "electronics"],
    "image": {
      "url": "https://example.com/laptop.jpg",
      "name": "Gaming Laptop Photo"
    }
  }'
```

#### Multiple Nested Models
```bash
curl -X PUT "http://localhost:8000/items/456/images" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Gaming Setup Bundle",
    "description": "Complete gaming setup with multiple components",
    "price": 2499.99,
    "tax": 250.00,
    "tags": ["gaming", "bundle", "setup"],
    "images": [
      {
        "url": "https://example.com/setup-front.jpg",
        "name": "Front View"
      },
      {
        "url": "https://example.com/setup-side.jpg",
        "name": "Side View"
      },
      {
        "url": "https://example.com/components.jpg",
        "name": "Individual Components"
      }
    ]
  }'
```

#### Dictionary Types
```bash
curl -X POST "http://localhost:8000/index-weights/" \
  -H "Content-Type: application/json" \
  -d '{
    "1": 0.8,
    "2": 1.2,
    "5": 0.5,
    "10": 2.0,
    "15": 1.5
  }'
```

### Data Structure Features

#### Collection Types
| Type | Purpose | Features | Example Use Case |
|------|---------|----------|------------------|
| `Set[str]` | Unique values | Auto-deduplication | Product tags, categories |
| `List[Model]` | Ordered collection | Maintains sequence | Image galleries, steps |
| `Dict[int, float]` | Key-value mapping | Type-validated pairs | Rankings, weights |

#### Validation Features
- **Nested Validation**: Each nested model fully validated
- **URL Validation**: HttpUrl ensures proper URL format
- **Type Conversion**: Automatic conversion where possible
- **Set Deduplication**: Duplicate tags automatically removed
- **Order Preservation**: Lists maintain item sequence

### Advanced Validation Examples

#### Valid Requests
```json
// Minimal required fields
{
  "name": "Simple Item",
  "price": 29.99
}

// With all optional fields
{
  "name": "Complete Item",
  "description": "Full featured item",
  "price": 99.99,
  "tax": 10.00,
  "tags": ["featured", "popular"],
  "image": {
    "url": "https://example.com/item.jpg",
    "name": "Item Photo"
  }
}
```

#### Validation Errors (422)
```bash
# Invalid URL format
{
  "name": "Item",
  "price": 99.99,
  "image": {
    "url": "not-a-valid-url",  # ❌ Invalid URL
    "name": "Photo"
  }
}

# Missing required nested fields
{
  "name": "Item",
  "price": 99.99,
  "image": {
    "url": "https://example.com/photo.jpg"
    # ❌ Missing required "name" field in Image
  }
}

# Invalid dictionary types
{
  "abc": 1.0,     # ❌ Key not convertible to int
  "1": "invalid"  # ❌ Value not convertible to float
}
```

### Real-World Use Cases

#### E-commerce Applications
- **Product Catalogs**: Items with image galleries
- **Category Management**: Nested category structures
- **Inventory Systems**: Complex product relationships

#### Content Management
- **Article Systems**: Posts with media attachments
- **Documentation**: Pages with multiple screenshots
- **Portfolio Sites**: Projects with image collections

#### Configuration Systems
- **Settings Management**: Hierarchical configuration
- **User Preferences**: Complex preference structures
- **System Configurations**: Nested parameter sets

### Key Learning Points
- **Nested models enable complex data relationships** while maintaining validation
- **Collections (List, Set, Dict) handle multiple related objects** efficiently
- **HttpUrl provides built-in URL validation** for web resource fields
- **Validation cascades through the entire hierarchy** automatically
- **Real-world APIs often require nested structures** for meaningful data representation
- **Pydantic handles complex type conversion** and validation seamlessly
- **Error messages pinpoint exact validation failures** in nested structures
- **Performance remains excellent** even with deep nesting and large collections

This lesson demonstrates enterprise-level API design patterns essential for building sophisticated applications that handle complex, real-world data relationships!

## Lesson 10: Extra Data Types

### Overview
- Advanced Python data types in FastAPI applications
- UUID (Universally Unique Identifier) for unique identifiers
- datetime objects for complete date and time information
- timedelta for time duration and intervals
- time objects for time-of-day without date
- Automatic type validation, conversion, and serialization
- Complex date/time calculations and scheduling systems

### File: `10extradatatypes.py`

This lesson demonstrates FastAPI's support for advanced Python data types including UUIDs, datetime objects, timedeltas, and time objects, with automatic validation and serialization.

### Key Concepts Covered
1. **UUID Type**: Unique identifier validation and conversion
2. **datetime Type**: Complete date/time with timezone support
3. **timedelta Type**: Duration and time interval calculations
4. **time Type**: Time-of-day representation without date
5. **Annotated Types**: Using Body() with advanced types
6. **Automatic Serialization**: JSON conversion of complex types
7. **Date/Time Arithmetic**: Complex calculations with temporal data

### Running the Application
```bash
fastapi dev 10extradatatypes.py
```

### Advanced Data Types

#### UUID (Universally Unique Identifier)
```python
item_id: UUID  # Path parameter with UUID validation
```
- **Format**: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
- **Validation**: Automatic UUID format checking
- **Use Cases**: Unique identifiers, database keys, session IDs

#### datetime (Date and Time)
```python
start_datetime: Annotated[datetime, Body()]
```
- **Format**: ISO 8601 (`2023-12-01T10:00:00`)
- **Features**: Timezone support, multiple input formats
- **Use Cases**: Timestamps, scheduling, event times

#### timedelta (Time Duration)
```python
process_after: Annotated[timedelta, Body()]
```
- **Format**: `HH:MM:SS` or `D days, HH:MM:SS`
- **Features**: Duration arithmetic, negative values
- **Use Cases**: Delays, intervals, processing time

#### time (Time of Day)
```python
repeat_at: Annotated[Union[time, None], Body()]
```
- **Format**: `HH:MM:SS` or `HH:MM`
- **Features**: Time without date, optional fields
- **Use Cases**: Daily schedules, recurring events

### Endpoint
- `PUT /items/{item_id}` - Configure item processing schedule with all advanced types

### Example Usage

#### Complete Request
```bash
curl -X PUT "http://localhost:8000/items/550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{
    "start_datetime": "2023-12-01T10:00:00",
    "end_datetime": "2023-12-01T15:30:00",
    "process_after": "01:30:00",
    "repeat_at": "09:00:00"
  }'
```

#### Response with Calculations
```json
{
  "item_id": "550e8400-e29b-41d4-a716-446655440000",
  "start_datetime": "2023-12-01T10:00:00",
  "end_datetime": "2023-12-01T15:30:00",
  "process_after": "01:30:00",
  "repeat_at": "09:00:00",
  "start_process": "2023-12-01T11:30:00",
  "duration": "04:00:00"
}
```

### Data Type Validation Examples

#### Valid Formats
```bash
# UUID formats
"550e8400-e29b-41d4-a716-446655440000" ✓
"6ba7b810-9dad-11d1-80b4-00c04fd430c8" ✓

# datetime formats
"2023-12-01T10:00:00" ✓
"2023-12-01T10:00:00Z" ✓ (UTC)
"2023-12-01T10:00:00+02:00" ✓ (with timezone)

# timedelta formats
"01:30:00" ✓ (1.5 hours)
"2 days, 03:45:30" ✓ (2 days, 3 hours, 45 minutes, 30 seconds)
"120" ✓ (120 seconds)

# time formats
"09:00:00" ✓
"14:30" ✓
null ✓ (optional field)
```

#### Validation Errors (422)
```bash
# Invalid UUID
curl -X PUT "http://localhost:8000/items/not-a-uuid" \
  -H "Content-Type: application/json" \
  -d '{"start_datetime": "2023-12-01T10:00:00", ...}'
# Returns: 422 "badly formed hexadecimal UUID string"

# Invalid datetime
curl -X PUT "http://localhost:8000/items/550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{
    "start_datetime": "2023-13-01T25:00:00",
    "end_datetime": "2023-12-01T15:30:00",
    "process_after": "01:30:00"
  }'
# Returns: 422 "invalid datetime format"

# Invalid timedelta
curl -X PUT "http://localhost:8000/items/550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{
    "start_datetime": "2023-12-01T10:00:00",
    "end_datetime": "2023-12-01T15:30:00",
    "process_after": "not-a-duration"
  }'
# Returns: 422 "invalid duration format"
```

### Date/Time Calculations

The endpoint performs automatic calculations:

```python
# Input values
start_datetime = "2023-12-01T10:00:00"
process_after = "01:30:00"  # 1.5 hours
end_datetime = "2023-12-01T15:30:00"

# Calculations
start_process = start_datetime + process_after  # "2023-12-01T11:30:00"
duration = end_datetime - start_process         # "04:00:00"
```

### Real-World Applications

#### Task Scheduling Systems
```json
{
  "start_datetime": "2023-12-01T08:00:00",
  "end_datetime": "2023-12-01T17:00:00",
  "process_after": "00:15:00",
  "repeat_at": "08:00:00"
}
```

#### Event Management
```json
{
  "start_datetime": "2023-12-15T19:00:00",
  "end_datetime": "2023-12-15T23:00:00",
  "process_after": "00:00:00",
  "repeat_at": null
}
```

#### Batch Processing
```json
{
  "start_datetime": "2023-12-01T02:00:00",
  "end_datetime": "2023-12-01T06:00:00", 
  "process_after": "01:00:00",
  "repeat_at": "02:00:00"
}
```

### Advanced Features

#### Automatic Type Conversion
- **JSON to Python**: FastAPI automatically converts JSON strings to Python objects
- **Python to JSON**: Response objects automatically serialized back to JSON
- **Timezone Handling**: datetime objects preserve timezone information
- **Validation**: Each type validated according to its specific format requirements

#### OpenAPI Documentation
- **Schema Generation**: All advanced types generate proper OpenAPI schemas
- **Example Values**: Automatic example generation for each data type
- **Format Specifications**: Clear format requirements in API documentation
- **Validation Rules**: Error conditions documented automatically

#### Error Handling
- **Type-Specific Errors**: Each data type provides specific error messages
- **Format Validation**: Clear feedback on format requirements
- **422 Status Codes**: Standard validation error responses
- **Detailed Messages**: Precise error descriptions for debugging

### Use Cases Summary

| Data Type | Primary Use Cases | Example Applications |
|-----------|------------------|---------------------|
| UUID | Unique identifiers | Database keys, session IDs, resource identifiers |
| datetime | Complete timestamps | Event scheduling, logging, audit trails |
| timedelta | Durations and delays | Processing windows, timeouts, intervals |
| time | Daily schedules | Recurring events, business hours, alarms |

### Key Learning Points
- **FastAPI handles advanced types automatically** with validation and serialization
- **UUID provides guaranteed unique identifiers** for distributed systems
- **datetime objects support timezone-aware** date and time operations
- **timedelta enables precise duration calculations** and time arithmetic
- **time objects perfect for daily scheduling** without date dependencies
- **Automatic JSON conversion** makes API responses clean and consistent
- **Validation errors provide clear guidance** for correct format usage
- **OpenAPI documentation** automatically includes proper type specifications
- **Real-world scheduling systems** require these advanced temporal data types

This lesson demonstrates how to build sophisticated time-based applications with proper data validation and complex temporal calculations!
