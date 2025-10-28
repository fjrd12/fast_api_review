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
├── 12extramodels.py
├── 13responseandstatuscode.py
├── 14requestforms.py
├── 15requestfiles.py
├── 16RequestFormFiles.py
├── 17HandlingErrors.py
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

## Lesson 12: Extra Models - Multiple Related Models

### Overview
- Creating multiple related Pydantic models for different use cases
- Model inheritance patterns and code reuse
- Separating input, output, and database models
- Password handling and security best practices
- Response model filtering for data protection
- Model composition and data transformation

### File: `12extramodels.py`

This lesson demonstrates how to create multiple related Pydantic models that serve different purposes in a FastAPI application, showcasing a common and powerful pattern for handling user data securely and efficiently.

### Key Concepts Covered
1. **Model Inheritance**: Using BaseModel inheritance for code reuse
2. **Separation of Concerns**: Different models for different purposes
3. **Password Security**: Proper handling of sensitive data
4. **Response Filtering**: Automatic exclusion of sensitive fields
5. **Data Transformation**: Converting between model types
6. **Email Validation**: Using EmailStr for email validation

### Running the Application
```bash
fastapi dev 12extramodels.py
```

### Model Design Pattern

This lesson implements a four-model pattern commonly used in production applications:

#### **UserBase Model (Base Class)**
```python
class UserBase(BaseModel):
    username: str
    email: EmailStr
```
- **Purpose**: Contains common fields shared across all user models
- **Benefits**: Promotes code reuse and ensures consistency
- **Fields**: Username and validated email address

#### **UserIn Model (Input)**
```python
class UserIn(UserBase):
    password: str
```
- **Purpose**: Accepts user input including raw password
- **Use Case**: API request validation
- **Security**: Contains plain text password (temporary)

#### **UserOut Model (Output)**
```python
class UserOut(UserBase):
    pass
```
- **Purpose**: Safe data for API responses
- **Security**: Excludes all password-related fields
- **Use Case**: Public API responses

#### **UserInDB Model (Database)**
```python
class UserInDB(UserBase):
    hashed_password: str
```
- **Purpose**: Database storage with hashed password
- **Security**: Contains hashed password instead of plain text
- **Use Case**: Internal data storage

### Data Flow and Security

#### **Complete User Creation Flow**
1. **Input**: Client sends `UserIn` with plain text password
2. **Processing**: Password gets hashed using security function
3. **Storage**: Data stored as `UserInDB` with hashed password
4. **Response**: Client receives `UserOut` without any password data

#### **Security Features**
- **Password Hashing**: Raw passwords are never stored
- **Response Filtering**: Passwords never appear in API responses
- **Email Validation**: Automatic email format validation
- **Type Safety**: Strong typing throughout the flow

### Example Usage

#### **Create User Request**
```bash
curl -X POST "http://localhost:8000/user/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "johndoe@example.com",
    "password": "supersecret123"
  }'
```

#### **Safe API Response**
```json
{
  "username": "johndoe",
  "email": "johndoe@example.com"
}
```

#### **Internal Database Storage**
```json
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "hashed_password": "supersecretsupersecret123"
}
```

### Key Functions

#### **Password Hashing Function**
```python
async def fake_password_hasher(raw_password: str) -> str:
    return "supersecret" + raw_password
```
- **Purpose**: Demonstrates password transformation
- **Note**: In production, use bcrypt, Argon2, or scrypt
- **Security**: Never store plain text passwords

#### **User Save Function**
```python
async def fake_save_user(user_in: UserIn) -> UserInDB:
    hashed_password = await fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
    return user_in_db
```
- **Purpose**: Converts input model to database model
- **Process**: Hashes password and creates database-ready object
- **Pattern**: Uses `model_dump()` for data conversion

### Advanced Patterns Demonstrated

#### **Model Composition with `model_dump()`**
```python
# Convert UserIn to dictionary and add hashed password
user_data = user_in.model_dump()  # Extract all fields
user_in_db = UserInDB(**user_data, hashed_password=hashed_password)
```

#### **Response Model Filtering**
```python
@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn) -> UserOut:
    user_saved = await fake_save_user(user_in)  # Returns UserInDB
    return user_saved  # Automatically filtered to UserOut
```

### Security Best Practices

#### **What This Pattern Prevents**
- **Password Exposure**: Passwords never appear in API responses
- **Data Leakage**: Sensitive fields are automatically excluded
- **Plain Text Storage**: Passwords are always hashed before storage
- **Accidental Disclosure**: Response models enforce safe data exposure

#### **Production Considerations**
- **Use Proper Hashing**: bcrypt, Argon2, or scrypt for password hashing
- **Environment Secrets**: Store hashing salts in environment variables
- **Database Constraints**: Add unique constraints for usernames/emails
- **Input Validation**: Additional validation for password complexity
- **Rate Limiting**: Prevent brute force attacks on user creation

### Real-World Applications

#### **User Management Systems**
- **Registration**: Safe user account creation
- **Authentication**: Secure password verification
- **Profile Updates**: Partial data updates without password exposure

#### **API Design Patterns**
- **Public APIs**: Clean response models for external consumption
- **Internal Services**: Rich data models for internal operations
- **Database Layer**: Optimized models for storage and retrieval

#### **Multi-Tenant Applications**
- **User Isolation**: Separate user contexts with clean models
- **Data Protection**: Automatic filtering of sensitive information
- **Compliance**: GDPR-compliant data handling patterns

### Validation and Error Handling

#### **Automatic Validations**
- **Email Format**: `EmailStr` ensures valid email addresses
- **Required Fields**: Pydantic validates all required fields
- **Type Checking**: Automatic type conversion and validation

#### **Error Responses**
```bash
# Invalid email format
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Benefits of This Pattern

#### **Development Benefits**
- **Code Reuse**: Base models eliminate duplication
- **Type Safety**: Strong typing prevents runtime errors
- **Clear Separation**: Each model has a single, clear purpose
- **Maintainability**: Changes to base model propagate automatically

#### **Security Benefits**
- **Automatic Protection**: Response models prevent data leakage
- **Consistent Handling**: Same security patterns across endpoints
- **Defense in Depth**: Multiple layers of data protection
- **Audit Trail**: Clear data transformation flow

#### **API Design Benefits**
- **Clean Interfaces**: Public APIs only expose necessary data
- **Backward Compatibility**: Internal changes don't affect public API
- **Documentation**: Models serve as living API documentation
- **Client Generation**: Type-safe client code generation

### Key Learning Points
- **Multiple models enable secure and flexible API design** with clear separation of concerns
- **Model inheritance promotes code reuse** while maintaining type safety
- **Response model filtering provides automatic security** against data leakage
- **Password hashing patterns ensure sensitive data protection** throughout the application
- **Pydantic model_dump() enables easy data transformation** between different model types
- **EmailStr provides built-in email validation** with clear error messages
- **This pattern scales well for complex applications** with multiple data representations
- **Security is built into the architecture** rather than being an afterthought

This lesson establishes the foundation for building secure, maintainable APIs with proper data separation and protection patterns that are essential for production applications!

## Lesson 13: Response Status Code - HTTP Status Code Management

### Overview
- Understanding and controlling HTTP status codes in FastAPI responses
- Using FastAPI's status module for semantic status codes
- RESTful API conventions for proper status code usage
- Client communication through meaningful status codes
- Best practices for status code selection and consistency

### File: `13responseandstatuscode.py`

This lesson demonstrates how to specify and control HTTP status codes in FastAPI responses, which is crucial for building RESTful APIs that communicate effectively with clients about the result of their requests.

### Key Concepts Covered
1. **Custom Status Codes**: Setting specific status codes using the status_code parameter
2. **FastAPI Status Module**: Using semantic constants instead of magic numbers
3. **HTTP Status Categories**: Understanding 1xx through 5xx status code ranges
4. **RESTful Conventions**: Proper status codes for different HTTP methods
5. **Client Communication**: How status codes inform API consumers
6. **Best Practices**: Consistency and semantic meaning in status code usage

### Running the Application
```bash
fastapi dev 13responseandstatuscode.py
```

### HTTP Status Code Categories

#### **1xx - Informational Responses**
- **100 Continue**: Request received, client should continue
- **101 Switching Protocols**: Server switching protocols

#### **2xx - Success Responses**
- **200 OK**: Standard successful response
- **201 Created**: Resource successfully created (POST operations)
- **202 Accepted**: Request accepted for processing (async operations)
- **204 No Content**: Successful request with no content to return (DELETE)

#### **3xx - Redirection Responses**
- **301 Moved Permanently**: Resource permanently moved
- **302 Found**: Resource temporarily moved
- **304 Not Modified**: Cached version is still valid

#### **4xx - Client Error Responses**
- **400 Bad Request**: Invalid request format or parameters
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Access denied
- **404 Not Found**: Resource not found
- **422 Unprocessable Entity**: Validation error (FastAPI default)

#### **5xx - Server Error Responses**
- **500 Internal Server Error**: Server-side error
- **502 Bad Gateway**: Invalid response from upstream server
- **503 Service Unavailable**: Server temporarily unavailable

### Endpoint Implementation

#### **Item Creation Endpoint**
```python
@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}
```

**Key Features:**
- **POST Method**: Appropriate for resource creation
- **201 Created Status**: Semantic status code for successful creation
- **Query Parameter**: Simple name parameter for item creation
- **JSON Response**: Returns created item data

### Example Usage

#### **Create Item Request**
```bash
curl -X POST "http://localhost:8000/items/?name=laptop" \
  -H "Content-Type: application/json"
```

#### **Successful Response**
```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "name": "laptop"
}
```

#### **Response Analysis**
- **Status Code**: 201 Created (not default 200 OK)
- **Semantic Meaning**: Indicates successful resource creation
- **Client Benefit**: Clear indication of operation result
- **REST Compliance**: Follows RESTful API conventions

### Status Code Best Practices

#### **RESTful API Status Code Conventions**
| HTTP Method | Operation | Success Status | Purpose |
|-------------|-----------|----------------|---------|
| POST | Create | 201 Created | Resource successfully created |
| GET | Read | 200 OK | Data retrieved successfully |
| PUT | Update | 200 OK | Resource updated successfully |
| PATCH | Partial Update | 200 OK | Resource partially updated |
| DELETE | Delete | 204 No Content | Resource deleted successfully |

#### **FastAPI Status Module Usage**
```python
from fastapi import status

# Recommended: Use semantic constants
@app.post("/items/", status_code=status.HTTP_201_CREATED)

# Avoid: Magic numbers
@app.post("/items/", status_code=201)
```

**Benefits of Status Constants:**
- **Self-Documenting**: Code clearly shows intent
- **IDE Support**: Autocompletion and type checking
- **Consistency**: Prevents typos and inconsistencies
- **Maintainability**: Easy to update across codebase

### Advanced Status Code Patterns

#### **Conditional Status Codes**
```python
from fastapi import HTTPException

@app.post("/items/")
async def create_item_advanced(name: str):
    if item_exists(name):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Item already exists"
        )
    
    create_item(name)
    return {"name": name, "status": "created"}
```

#### **Multiple Success Scenarios**
```python
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    if not item_exists(item_id):
        # Create new resource
        create_item(item_id, item)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Item created"}
        )
    else:
        # Update existing resource
        update_existing_item(item_id, item)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Item updated"}
        )
```

### Error Handling with Status Codes

#### **Client Errors (4xx)**
```python
# Validation Error Example
{
  "detail": [
    {
      "loc": ["query", "name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
# Status: 422 Unprocessable Entity
```

#### **Custom Error Responses**
```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Item ID must be positive"
        )
    
    item = find_item(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    return item
```

### Real-World Applications

#### **E-commerce API**
- **201 Created**: New product added to catalog
- **200 OK**: Product details retrieved
- **400 Bad Request**: Invalid product data
- **404 Not Found**: Product doesn't exist
- **409 Conflict**: Product SKU already exists

#### **User Management API**
- **201 Created**: User account created
- **200 OK**: User profile retrieved
- **401 Unauthorized**: Login required
- **403 Forbidden**: Insufficient permissions
- **422 Unprocessable Entity**: Invalid email format

#### **File Upload API**
- **201 Created**: File uploaded successfully
- **202 Accepted**: File queued for processing
- **413 Payload Too Large**: File size exceeds limit
- **415 Unsupported Media Type**: Invalid file format

### API Documentation Benefits

#### **Automatic OpenAPI Documentation**
```python
@app.post(
    "/items/", 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new item",
    description="Creates a new item with the specified name",
    responses={
        201: {"description": "Item created successfully"},
        400: {"description": "Invalid item name"},
        409: {"description": "Item already exists"}
    }
)
```

#### **Client Code Generation**
Status codes enable:
- **Type-safe client libraries**: Generated clients handle status codes correctly
- **Error handling**: Clients can respond appropriately to different status codes
- **API contracts**: Clear expectations between client and server

### Testing with Status Codes

#### **Test Examples**
```python
def test_create_item_success():
    response = client.post("/items/?name=test")
    assert response.status_code == 201
    assert response.json() == {"name": "test"}

def test_create_item_validation_error():
    response = client.post("/items/")  # Missing name parameter
    assert response.status_code == 422
```

### Performance and Monitoring

#### **Status Code Metrics**
- **Success Rate**: Percentage of 2xx responses
- **Error Rate**: Percentage of 4xx/5xx responses
- **API Health**: Monitor status code distributions
- **Client Debugging**: Status codes help identify issues

#### **Logging and Observability**
```python
import logging

@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    logging.info(f"Creating item: {name}")
    result = {"name": name}
    logging.info(f"Item created successfully: {result}")
    return result
```

### Key Learning Points
- **Proper status codes improve API usability** and client integration
- **FastAPI's status module provides semantic constants** for better code quality
- **RESTful conventions guide status code selection** for different operations
- **201 Created is the correct status for resource creation** instead of default 200 OK
- **Status codes communicate operation results** without clients parsing response bodies
- **Consistent status code usage** improves API predictability and developer experience
- **Error status codes enable proper client error handling** and user feedback
- **Status codes are part of the API contract** and should be documented and tested

This lesson establishes the foundation for building well-designed APIs that communicate effectively with clients through proper HTTP status code usage, improving both developer experience and application reliability!

---

## Lesson 14: Request Forms

### Overview
- **Purpose**: Learn how to receive form data instead of JSON in FastAPI endpoints
- **Key Concept**: Using `Form()` to handle HTML form submissions and `application/x-www-form-urlencoded` data
- **Use Case**: Building traditional web forms, login systems, and file upload interfaces

### File: `14requestforms.py`

This lesson demonstrates how to handle form data in FastAPI applications using the `Form` class, which is essential for building web applications that need to process HTML form submissions.

### Core Concepts

#### **Form Data vs JSON**
```python
# JSON Request (previous lessons)
{"username": "john", "password": "secret"}

# Form Data (this lesson) 
# Content-Type: application/x-www-form-urlencoded
# username=john&password=secret
```

#### **The Form Import**
```python
from fastapi import FastAPI, Form

app = FastAPI()
```

### Implementation Details

#### **Login Endpoint with Form Data**
```python
@app.post("/login/")
async def login(username: str = Form(), password: str = Form()):
    """
    User login endpoint accepting form data.
    
    This endpoint demonstrates how to receive form data using FastAPI's Form class.
    It accepts 'username' and 'password' as form fields in a POST request and
    returns a simple dictionary containing the provided username.
    
    Args:
        username (str): The username provided in the form data
        password (str): The password provided in the form data
    """
    return {"username": username, "message": "Login successful!"}
```

### Form Data Characteristics

#### **Content Type**
- **Form Data**: `application/x-www-form-urlencoded`
- **JSON Data**: `application/json`
- **Multipart Forms**: `multipart/form-data` (used with file uploads)

#### **Data Format**
```
# URL-encoded form data
username=johndoe&password=mysecretpassword&email=john%40example.com
```

### HTML Form Example

#### **Frontend HTML Form**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Login Form</title>
</head>
<body>
    <form action="/login/" method="post">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required>
        
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required>
        
        <button type="submit">Login</button>
    </form>
</body>
</html>
```

### Advanced Form Patterns

#### **Form with Validation**
```python
from fastapi import FastAPI, Form, HTTPException
from pydantic import EmailStr

@app.post("/register/")
async def register(
    username: str = Form(min_length=3, max_length=20),
    email: EmailStr = Form(),
    password: str = Form(min_length=8),
    confirm_password: str = Form()
):
    if password != confirm_password:
        raise HTTPException(
            status_code=400, 
            detail="Passwords do not match"
        )
    
    return {
        "username": username,
        "email": email,
        "message": "Registration successful!"
    }
```

#### **Optional Form Fields**
```python
@app.post("/profile/")
async def update_profile(
    name: str = Form(),
    bio: str = Form(None),  # Optional field
    age: int = Form(None),  # Optional field
    newsletter: bool = Form(False)  # Checkbox with default
):
    profile_data = {"name": name, "newsletter": newsletter}
    
    if bio:
        profile_data["bio"] = bio
    if age:
        profile_data["age"] = age
    
    return profile_data
```

### Testing Form Endpoints

#### **Using curl**
```bash
# Test the login endpoint
curl -X POST "http://localhost:8000/login/" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=johndoe&password=secret123"
```

#### **Using Python requests**
```python
import requests

# Form data submission
response = requests.post(
    "http://localhost:8000/login/",
    data={
        "username": "johndoe",
        "password": "secret123"
    }
)

print(response.json())
# Output: {"username": "johndoe", "message": "Login successful!"}
```

#### **Using FastAPI TestClient**
```python
from fastapi.testclient import TestClient

def test_login_form():
    client = TestClient(app)
    response = client.post(
        "/login/",
        data={"username": "testuser", "password": "testpass"}
    )
    
    assert response.status_code == 200
    assert response.json() == {
        "username": "testuser", 
        "message": "Login successful!"
    }
```

### Form Data vs JSON Comparison

| Feature | Form Data | JSON |
|---------|-----------|------|
| **Content-Type** | `application/x-www-form-urlencoded` | `application/json` |
| **Browser Support** | Native HTML forms | JavaScript required |
| **File Uploads** | Requires `multipart/form-data` | Not supported |
| **Nested Objects** | Limited support | Full support |
| **Arrays** | Complex syntax | Native support |
| **Use Cases** | Traditional web forms, login pages | REST APIs, SPAs |

### When to Use Form Data

#### **Ideal Scenarios**
- **Traditional web applications** with server-side rendering
- **Login and authentication** forms
- **File upload** interfaces (with multipart forms)
- **Progressive enhancement** where JavaScript might be disabled
- **SEO-friendly forms** that work without JavaScript

#### **Not Ideal For**
- **Complex nested data** structures
- **REST API** endpoints primarily consumed by JavaScript
- **Mobile applications** that prefer JSON
- **Real-time applications** requiring WebSocket connections

### Security Considerations

#### **CSRF Protection**
```python
from fastapi import FastAPI, Form, Depends
from fastapi.security import HTTPBasic

security = HTTPBasic()

@app.post("/secure-login/")
async def secure_login(
    username: str = Form(),
    password: str = Form(),
    credentials: HTTPBasicCredentials = Depends(security)
):
    # Additional security layer
    return {"username": username, "authenticated": True}
```

#### **Input Validation**
```python
import re

@app.post("/safe-login/")
async def safe_login(
    username: str = Form(regex=r"^[a-zA-Z0-9_]+$"),
    password: str = Form(min_length=8)
):
    # Username only allows alphanumeric and underscore
    # Password must be at least 8 characters
    return {"username": username, "status": "validated"}
```

### Real-World Applications

#### **User Authentication System**
```python
@app.post("/auth/login/")
async def authenticate_user(
    email: EmailStr = Form(),
    password: str = Form(),
    remember_me: bool = Form(False)
):
    # Hash and verify password
    # Create session or JWT token
    # Handle "remember me" functionality
    return {
        "email": email,
        "authenticated": True,
        "remember_me": remember_me,
        "token": "jwt_token_here"
    }
```

#### **Contact Form**
```python
@app.post("/contact/")
async def contact_form(
    name: str = Form(),
    email: EmailStr = Form(),
    subject: str = Form(),
    message: str = Form(max_length=1000),
    phone: str = Form(None)
):
    # Send email notification
    # Store in database
    # Return confirmation
    return {
        "name": name,
        "email": email,
        "subject": subject,
        "message": "Thank you for your message! We'll get back to you soon."
    }
```

### Integration with Frontend Frameworks

#### **Working with HTMX**
```html
<!-- HTMX form with dynamic response -->
<form hx-post="/login/" hx-target="#result">
    <input type="text" name="username" placeholder="Username" required>
    <input type="password" name="password" placeholder="Password" required>
    <button type="submit">Login</button>
</form>
<div id="result"></div>
```

#### **Progressive Enhancement**
```python
@app.post("/login/")
async def login(
    request: Request,
    username: str = Form(),
    password: str = Form()
):
    # Authenticate user
    result = {"username": username, "message": "Login successful!"}
    
    # Check if request expects JSON (AJAX) or HTML
    if "application/json" in request.headers.get("accept", ""):
        return result
    else:
        # Return HTML template for traditional form submission
        return templates.TemplateResponse(
            "login_success.html", 
            {"request": request, **result}
        )
```

### Key Learning Points
- **Form data is essential** for traditional web applications and HTML forms
- **`Form()` class handles URL-encoded form data** instead of JSON payloads
- **Form validation works similarly** to JSON validation with Pydantic
- **Content-Type matters** - forms use `application/x-www-form-urlencoded`
- **Browser compatibility** - forms work without JavaScript
- **Security considerations** apply to form data just like JSON data
- **Testing form endpoints** requires proper content-type headers
- **Progressive enhancement** allows forms to work with and without JavaScript
- **Form data is ideal** for authentication, file uploads, and traditional web interfaces

This lesson provides the foundation for building web applications that can handle both modern JSON APIs and traditional HTML form submissions, ensuring broad compatibility and accessibility!

---

## Lesson 15: Request Files

### Overview
- **Purpose**: Learn how to handle file uploads in FastAPI applications
- **Key Concepts**: Using `File()` and `UploadFile` for different file handling scenarios
- **Use Cases**: Document uploads, image processing, data import systems, and file storage services

### File: `15requestfiles.py`

This lesson demonstrates two different approaches to handling file uploads in FastAPI: using `File()` for reading files as bytes and `UploadFile` for more efficient file handling with metadata access.

### Core Concepts

#### **File Upload Methods**
```python
# Method 1: File as bytes (small files)
file: bytes = File()

# Method 2: UploadFile object (recommended for larger files)
file: UploadFile
```

#### **Required Imports**
```python
from fastapi import FastAPI, File, UploadFile

app = FastAPI()
```

### Implementation Details

#### **File Upload as Bytes**
```python
@app.post("/files/")
async def create_file(file: bytes = File()):
    """
    Upload a file and return its size.
    
    This endpoint demonstrates how to handle file uploads in FastAPI using
    the File class. The uploaded file is read as bytes, and the size of
    the file is returned in the response.
    
    Args:
        file (bytes): The uploaded file content as bytes
        
    Returns:
        dict: A dictionary containing the size of the uploaded file in bytes
    """
    return {"file_size": len(file)}
```

#### **File Upload as UploadFile Object**
```python
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    """
    Upload a file and return its filename.
    
    This endpoint demonstrates how to handle file uploads in FastAPI using
    the UploadFile class. The uploaded file is represented as an UploadFile
    object, which provides access to metadata such as the filename.
    
    Args:
        file (UploadFile): The uploaded file as an UploadFile object
        
    Returns:
        dict: A dictionary containing the filename of the uploaded file
    """
    return {"filename": file.filename}
```

### File Upload Comparison

| Feature | `File()` (bytes) | `UploadFile` |
|---------|------------------|--------------|
| **Memory Usage** | Loads entire file into memory | Streams file content |
| **Performance** | Good for small files | Better for large files |
| **Metadata Access** | Limited | Full metadata available |
| **File Operations** | Basic byte operations | Rich file-like interface |
| **Best For** | Small files, simple processing | Large files, complex operations |

### UploadFile Properties and Methods

#### **Available Properties**
```python
@app.post("/file-info/")
async def get_file_info(file: UploadFile):
    return {
        "filename": file.filename,           # Original filename
        "content_type": file.content_type,   # MIME type
        "size": file.size,                   # File size (if available)
        "headers": dict(file.headers)        # All headers
    }
```

#### **Reading File Content**
```python
@app.post("/process-file/")
async def process_file(file: UploadFile):
    # Read entire file content
    content = await file.read()
    
    # Reset file pointer to beginning
    await file.seek(0)
    
    # Read line by line (for text files)
    lines = []
    async for line in file:
        lines.append(line.decode())
    
    return {
        "filename": file.filename,
        "size": len(content),
        "lines_count": len(lines)
    }
```

### Advanced File Handling Patterns

#### **Multiple File Uploads**
```python
from typing import List

@app.post("/multiple-files/")
async def upload_multiple_files(files: List[UploadFile]):
    """Handle multiple file uploads simultaneously."""
    file_info = []
    
    for file in files:
        content = await file.read()
        file_info.append({
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(content)
        })
    
    return {"uploaded_files": file_info}
```

#### **File Validation**
```python
from fastapi import HTTPException

ALLOWED_EXTENSIONS = {".txt", ".pdf", ".doc", ".docx", ".jpg", ".png"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@app.post("/validated-upload/")
async def upload_with_validation(file: UploadFile):
    """Upload file with validation for type and size."""
    
    # Check file extension
    if not any(file.filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Read and check file size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE // (1024*1024)}MB"
        )
    
    # Reset file pointer for further processing
    await file.seek(0)
    
    return {
        "filename": file.filename,
        "size": len(content),
        "message": "File uploaded successfully"
    }
```

#### **File Storage**
```python
import aiofiles
import os
from pathlib import Path

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/save-file/")
async def save_uploaded_file(file: UploadFile):
    """Save uploaded file to disk."""
    
    file_path = UPLOAD_DIR / file.filename
    
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    return {
        "filename": file.filename,
        "saved_path": str(file_path),
        "message": "File saved successfully"
    }
```

### Content Type Handling

#### **Image Processing Example**
```python
from PIL import Image
import io

@app.post("/process-image/")
async def process_image(file: UploadFile):
    """Process uploaded image file."""
    
    # Verify it's an image
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400,
            detail="File must be an image"
        )
    
    # Read image content
    content = await file.read()
    
    # Process with PIL
    image = Image.open(io.BytesIO(content))
    
    return {
        "filename": file.filename,
        "format": image.format,
        "mode": image.mode,
        "size": image.size,
        "content_type": file.content_type
    }
```

#### **CSV Processing Example**
```python
import csv
import io

@app.post("/process-csv/")
async def process_csv(file: UploadFile):
    """Process uploaded CSV file."""
    
    if not file.filename.lower().endswith('.csv'):
        raise HTTPException(
            status_code=400,
            detail="File must be a CSV file"
        )
    
    content = await file.read()
    csv_data = content.decode('utf-8')
    
    # Parse CSV
    csv_reader = csv.DictReader(io.StringIO(csv_data))
    rows = list(csv_reader)
    
    return {
        "filename": file.filename,
        "rows_count": len(rows),
        "columns": list(rows[0].keys()) if rows else [],
        "sample_data": rows[:3]  # First 3 rows as sample
    }
```

### Testing File Uploads

#### **Using curl**
```bash
# Upload a single file
curl -X POST "http://localhost:8000/files/" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@example.txt"

# Upload with UploadFile endpoint
curl -X POST "http://localhost:8000/uploadfile/" \
     -F "file=@document.pdf"
```

#### **Using Python requests**
```python
import requests

# Upload file with requests
with open('test_file.txt', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'http://localhost:8000/uploadfile/',
        files=files
    )
    
print(response.json())
```

#### **Using FastAPI TestClient**
```python
from fastapi.testclient import TestClient
import io

def test_file_upload():
    client = TestClient(app)
    
    # Create test file
    test_file = io.BytesIO(b"test file content")
    test_file.name = "test.txt"
    
    response = client.post(
        "/uploadfile/",
        files={"file": ("test.txt", test_file, "text/plain")}
    )
    
    assert response.status_code == 200
    assert response.json() == {"filename": "test.txt"}
```

### HTML Form for File Upload

#### **Frontend Form Example**
```html
<!DOCTYPE html>
<html>
<head>
    <title>File Upload</title>
</head>
<body>
    <h2>Upload File</h2>
    <form action="/uploadfile/" method="post" enctype="multipart/form-data">
        <label for="file">Choose file:</label>
        <input type="file" id="file" name="file" required>
        <button type="submit">Upload</button>
    </form>
    
    <h2>Upload Multiple Files</h2>
    <form action="/multiple-files/" method="post" enctype="multipart/form-data">
        <label for="files">Choose files:</label>
        <input type="file" id="files" name="files" multiple required>
        <button type="submit">Upload All</button>
    </form>
</body>
</html>
```

### Security Considerations

#### **File Validation Best Practices**
```python
import magic
from pathlib import Path

async def validate_file_security(file: UploadFile):
    """Comprehensive file validation for security."""
    
    # Check filename for path traversal attacks
    if ".." in file.filename or "/" in file.filename:
        raise HTTPException(400, "Invalid filename")
    
    # Read file content
    content = await file.read()
    await file.seek(0)
    
    # Validate file signature (magic numbers)
    file_type = magic.from_buffer(content, mime=True)
    allowed_types = ["image/jpeg", "image/png", "text/plain", "application/pdf"]
    
    if file_type not in allowed_types:
        raise HTTPException(400, f"File type {file_type} not allowed")
    
    # Check for malicious content (basic example)
    if b"<script>" in content.lower():
        raise HTTPException(400, "Potentially malicious content detected")
    
    return True

@app.post("/secure-upload/")
async def secure_file_upload(file: UploadFile):
    """Secure file upload with comprehensive validation."""
    
    await validate_file_security(file)
    
    # Generate secure filename
    secure_filename = f"{uuid4()}_{file.filename}"
    
    return {
        "original_filename": file.filename,
        "secure_filename": secure_filename,
        "message": "File uploaded securely"
    }
```

### Performance Considerations

#### **Streaming Large Files**
```python
@app.post("/stream-upload/")
async def stream_large_file(file: UploadFile):
    """Handle large file uploads with streaming."""
    
    file_path = UPLOAD_DIR / file.filename
    
    async with aiofiles.open(file_path, 'wb') as f:
        while chunk := await file.read(1024):  # Read in 1KB chunks
            await f.write(chunk)
    
    return {
        "filename": file.filename,
        "message": "Large file uploaded successfully"
    }
```

#### **Background Processing**
```python
from fastapi import BackgroundTasks

def process_file_background(filename: str):
    """Background task for file processing."""
    # Simulate file processing
    time.sleep(10)
    print(f"Finished processing {filename}")

@app.post("/upload-and-process/")
async def upload_with_background_processing(
    file: UploadFile, 
    background_tasks: BackgroundTasks
):
    """Upload file and process it in the background."""
    
    # Save file
    file_path = UPLOAD_DIR / file.filename
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    # Add background processing task
    background_tasks.add_task(process_file_background, file.filename)
    
    return {
        "filename": file.filename,
        "message": "File uploaded, processing started in background"
    }
```

### Real-World Applications

#### **Document Management System**
```python
@app.post("/documents/")
async def upload_document(
    file: UploadFile,
    category: str = Form(),
    description: str = Form(None)
):
    """Upload document with metadata."""
    
    # Validate document type
    allowed_types = [".pdf", ".doc", ".docx", ".txt"]
    if not any(file.filename.lower().endswith(ext) for ext in allowed_types):
        raise HTTPException(400, "Invalid document type")
    
    # Save file and metadata
    document_id = str(uuid4())
    file_path = UPLOAD_DIR / f"{document_id}_{file.filename}"
    
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    # Store metadata in database (simulated)
    document_metadata = {
        "id": document_id,
        "filename": file.filename,
        "category": category,
        "description": description,
        "upload_date": datetime.now().isoformat(),
        "file_path": str(file_path)
    }
    
    return document_metadata
```

#### **Image Upload Service**
```python
@app.post("/images/")
async def upload_image(file: UploadFile):
    """Upload and process image with thumbnail generation."""
    
    if not file.content_type.startswith('image/'):
        raise HTTPException(400, "File must be an image")
    
    content = await file.read()
    image = Image.open(io.BytesIO(content))
    
    # Generate thumbnail
    thumbnail = image.copy()
    thumbnail.thumbnail((200, 200))
    
    # Save original and thumbnail
    image_id = str(uuid4())
    original_path = UPLOAD_DIR / f"{image_id}_original.jpg"
    thumbnail_path = UPLOAD_DIR / f"{image_id}_thumbnail.jpg"
    
    image.save(original_path, "JPEG")
    thumbnail.save(thumbnail_path, "JPEG")
    
    return {
        "image_id": image_id,
        "original_filename": file.filename,
        "size": image.size,
        "format": image.format,
        "original_url": f"/images/{image_id}/original",
        "thumbnail_url": f"/images/{image_id}/thumbnail"
    }
```

### Key Learning Points
- **`File()` is suitable for small files** that can be loaded entirely into memory as bytes
- **`UploadFile` is preferred for larger files** and provides rich metadata and streaming capabilities
- **File validation is crucial** for security - check extensions, content types, and file signatures
- **Content-Type must be `multipart/form-data`** for file uploads, not JSON
- **Streaming large files** prevents memory issues and improves performance
- **Background processing** can handle time-consuming file operations without blocking responses
- **Security considerations** include path traversal prevention and malicious content detection
- **Testing file uploads** requires proper multipart form data simulation
- **UploadFile provides metadata access** including filename, content type, and headers
- **File storage patterns** should include unique naming and organized directory structures

This lesson establishes the foundation for building robust file upload systems that can handle various file types securely and efficiently, from simple document uploads to complex image processing pipelines!

---

## Lesson 16: Request Form and Files

### Overview
- **Purpose**: Learn how to handle both form data and file uploads simultaneously in a single endpoint
- **Key Concepts**: Combining `Form()` and `File()` parameters with `Annotated` type hints
- **Use Cases**: Document upload with metadata, user registration with profile pictures, multi-part data submission

### File: `16RequestFormFiles.py`

This lesson demonstrates how to create endpoints that accept both form fields and file uploads in the same request, using modern Python type annotations with `Annotated` for clear parameter definitions.

### Core Concepts

#### **Mixed Form and File Data**
```python
# Single endpoint accepting both files and form data
@app.post("/files/")
async def create_file(
    file: Annotated[bytes, File()],          # File as bytes
    fileb: Annotated[UploadFile, File()],    # File as UploadFile
    token: Annotated[str, Form()]            # Form field
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type
    }
```

#### **Required Imports**
```python
from typing import Annotated
from fastapi import FastAPI, File, Form, UploadFile

app = FastAPI()
```

### Implementation Analysis

#### **The Complete Endpoint**
```python
@app.post("/files/")
async def create_file(
    file: Annotated[bytes, File()],
    fileb: Annotated[UploadFile, File()],
    token: Annotated[str, Form()]
):
    """
    Upload files with form data in a single request.
    
    This endpoint demonstrates how to handle multiple types of data in one request:
    - A file uploaded as bytes (for small files)
    - A file uploaded as UploadFile (for larger files with metadata)
    - A form field containing a token string
    
    Args:
        file (bytes): Small file uploaded as bytes
        fileb (UploadFile): File with metadata access
        token (str): Authentication token or form data
        
    Returns:
        dict: Information about uploaded files and form data
        
    Example Request:
        POST /files/
        Content-Type: multipart/form-data
        file: <small_file.txt>
        fileb: <large_document.pdf>
        token: "auth_token_12345"
        
    Example Response:
        {
            "file_size": 1024,
            "token": "auth_token_12345",
            "fileb_content_type": "application/pdf"
        }
    """
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type
    }
```

### Annotated Type Hints

#### **Why Use Annotated?**
```python
# Old style (still works)
async def old_style(file: bytes = File(), token: str = Form()):
    pass

# New style with Annotated (recommended)
async def new_style(
    file: Annotated[bytes, File()],
    token: Annotated[str, Form()]
):
    pass
```

#### **Benefits of Annotated**
- **Clearer separation** between type and FastAPI metadata
- **Better IDE support** for type checking and autocompletion
- **More explicit** about parameter requirements
- **Future-proof** with Python's type system evolution

### Advanced Mixed Data Patterns

#### **Document Upload with Metadata**
```python
from typing import Optional
from datetime import datetime

@app.post("/documents/")
async def upload_document(
    document: Annotated[UploadFile, File(description="Document file to upload")],
    title: Annotated[str, Form(description="Document title")],
    description: Annotated[Optional[str], Form()] = None,
    category: Annotated[str, Form(description="Document category")],
    tags: Annotated[Optional[str], Form(description="Comma-separated tags")] = None,
    is_public: Annotated[bool, Form()] = False
):
    """Upload document with comprehensive metadata."""
    
    # Process tags
    tag_list = tags.split(",") if tags else []
    
    # Validate file type
    allowed_types = ["application/pdf", "text/plain", "application/msword"]
    if document.content_type not in allowed_types:
        raise HTTPException(400, f"File type {document.content_type} not allowed")
    
    # Read file content
    content = await document.read()
    
    return {
        "document_info": {
            "filename": document.filename,
            "content_type": document.content_type,
            "size": len(content)
        },
        "metadata": {
            "title": title,
            "description": description,
            "category": category,
            "tags": tag_list,
            "is_public": is_public,
            "upload_timestamp": datetime.now().isoformat()
        }
    }
```

#### **User Profile with Avatar**
```python
from pydantic import EmailStr

@app.post("/profile/")
async def create_profile(
    avatar: Annotated[UploadFile, File(description="Profile picture")],
    username: Annotated[str, Form(min_length=3, max_length=20)],
    email: Annotated[EmailStr, Form()],
    bio: Annotated[Optional[str], Form(max_length=500)] = None,
    age: Annotated[Optional[int], Form(ge=13, le=120)] = None,
    newsletter: Annotated[bool, Form()] = False
):
    """Create user profile with avatar upload."""
    
    # Validate avatar is an image
    if not avatar.content_type.startswith('image/'):
        raise HTTPException(400, "Avatar must be an image file")
    
    # Process avatar
    avatar_content = await avatar.read()
    if len(avatar_content) > 5 * 1024 * 1024:  # 5MB limit
        raise HTTPException(413, "Avatar file too large (max 5MB)")
    
    return {
        "profile": {
            "username": username,
            "email": email,
            "bio": bio,
            "age": age,
            "newsletter_subscribed": newsletter
        },
        "avatar": {
            "filename": avatar.filename,
            "content_type": avatar.content_type,
            "size": len(avatar_content)
        }
    }
```

#### **Multiple Files with Form Data**
```python
@app.post("/batch-upload/")
async def batch_upload(
    files: Annotated[List[UploadFile], File(description="Multiple files to upload")],
    project_name: Annotated[str, Form(description="Project name")],
    description: Annotated[str, Form(description="Project description")],
    category: Annotated[str, Form(description="Project category")],
    notify_users: Annotated[bool, Form()] = True
):
    """Upload multiple files with project metadata."""
    
    uploaded_files = []
    total_size = 0
    
    for file in files:
        content = await file.read()
        file_size = len(content)
        total_size += file_size
        
        uploaded_files.append({
            "filename": file.filename,
            "content_type": file.content_type,
            "size": file_size
        })
        
        # Reset file pointer if needed for further processing
        await file.seek(0)
    
    return {
        "project": {
            "name": project_name,
            "description": description,
            "category": category,
            "notify_users": notify_users
        },
        "upload_summary": {
            "files_count": len(files),
            "total_size": total_size,
            "files": uploaded_files
        }
    }
```

### Form Validation with Files

#### **Complex Validation Example**
```python
from fastapi import HTTPException, status

@app.post("/submit-application/")
async def submit_application(
    resume: Annotated[UploadFile, File(description="Resume/CV file")],
    cover_letter: Annotated[Optional[UploadFile], File(description="Cover letter")] = None,
    full_name: Annotated[str, Form(min_length=2, max_length=100)],
    email: Annotated[EmailStr, Form()],
    phone: Annotated[str, Form(regex=r'^\+?[\d\s\-\(\)]+$')],
    position: Annotated[str, Form(description="Position applied for")],
    experience_years: Annotated[int, Form(ge=0, le=50)],
    salary_expectation: Annotated[Optional[int], Form(ge=0)] = None,
    available_start: Annotated[str, Form(description="Available start date (YYYY-MM-DD)")],
    relocate_willing: Annotated[bool, Form()] = False
):
    """Submit job application with resume and form data."""
    
    # Validate resume file
    if resume.content_type not in ["application/pdf", "application/msword", 
                                  "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume must be PDF or Word document"
        )
    
    resume_content = await resume.read()
    if len(resume_content) > 10 * 1024 * 1024:  # 10MB limit
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Resume file too large (max 10MB)"
        )
    
    # Validate cover letter if provided
    cover_letter_info = None
    if cover_letter:
        if cover_letter.content_type not in ["application/pdf", "text/plain"]:
            raise HTTPException(400, "Cover letter must be PDF or text file")
        
        cover_letter_content = await cover_letter.read()
        cover_letter_info = {
            "filename": cover_letter.filename,
            "size": len(cover_letter_content)
        }
    
    # Validate start date format
    try:
        datetime.strptime(available_start, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(400, "Invalid date format. Use YYYY-MM-DD")
    
    return {
        "application": {
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "position": position,
            "experience_years": experience_years,
            "salary_expectation": salary_expectation,
            "available_start": available_start,
            "relocate_willing": relocate_willing
        },
        "documents": {
            "resume": {
                "filename": resume.filename,
                "size": len(resume_content)
            },
            "cover_letter": cover_letter_info
        },
        "status": "Application submitted successfully"
    }
```

### Testing Mixed Form and File Data

#### **Using curl**
```bash
# Test the basic endpoint
curl -X POST "http://localhost:8000/files/" \
     -F "file=@small_file.txt" \
     -F "fileb=@large_document.pdf" \
     -F "token=auth_token_12345"

# Test document upload with metadata
curl -X POST "http://localhost:8000/documents/" \
     -F "document=@report.pdf" \
     -F "title=Monthly Report" \
     -F "description=Sales analysis for March" \
     -F "category=business" \
     -F "tags=sales,analysis,monthly" \
     -F "is_public=false"
```

#### **Using Python requests**
```python
import requests

# Test multiple data types
files = {
    'file': ('test.txt', open('test.txt', 'rb'), 'text/plain'),
    'fileb': ('document.pdf', open('document.pdf', 'rb'), 'application/pdf')
}

data = {
    'token': 'auth_token_12345'
}

response = requests.post(
    'http://localhost:8000/files/',
    files=files,
    data=data
)

print(response.json())
```

#### **Using FastAPI TestClient**
```python
from fastapi.testclient import TestClient
import io

def test_mixed_form_file_upload():
    client = TestClient(app)
    
    # Create test files
    small_file = io.BytesIO(b"small file content")
    large_file = io.BytesIO(b"large file content for upload")
    
    response = client.post(
        "/files/",
        files={
            "file": ("small.txt", small_file, "text/plain"),
            "fileb": ("large.pdf", large_file, "application/pdf")
        },
        data={"token": "test_token"}
    )
    
    assert response.status_code == 200
    result = response.json()
    assert result["token"] == "test_token"
    assert result["file_size"] == 18
    assert result["fileb_content_type"] == "application/pdf"
```

### HTML Form Example

#### **Frontend Form with Files and Data**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Upload Files with Data</title>
</head>
<body>
    <h2>Upload Files with Metadata</h2>
    <form action="/documents/" method="post" enctype="multipart/form-data">
        <!-- File uploads -->
        <label for="document">Document:</label>
        <input type="file" id="document" name="document" accept=".pdf,.doc,.docx" required>
        
        <!-- Form fields -->
        <label for="title">Title:</label>
        <input type="text" id="title" name="title" required>
        
        <label for="description">Description:</label>
        <textarea id="description" name="description" rows="3"></textarea>
        
        <label for="category">Category:</label>
        <select id="category" name="category" required>
            <option value="business">Business</option>
            <option value="technical">Technical</option>
            <option value="legal">Legal</option>
        </select>
        
        <label for="tags">Tags (comma-separated):</label>
        <input type="text" id="tags" name="tags" placeholder="tag1, tag2, tag3">
        
        <label>
            <input type="checkbox" name="is_public" value="true">
            Make document public
        </label>
        
        <button type="submit">Upload Document</button>
    </form>
</body>
</html>
```

### Security and Validation Best Practices

#### **Comprehensive Security Example**
```python
import hashlib
import secrets
from pathlib import Path

UPLOAD_DIR = Path("secure_uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/secure-upload/")
async def secure_mixed_upload(
    file: Annotated[UploadFile, File()],
    user_id: Annotated[int, Form(gt=0)],
    api_key: Annotated[str, Form(min_length=32)],
    checksum: Annotated[str, Form(description="SHA256 checksum of file")]
):
    """Secure file upload with integrity verification."""
    
    # Validate API key (simplified example)
    if not validate_api_key(api_key, user_id):
        raise HTTPException(401, "Invalid API key")
    
    # Read file content
    content = await file.read()
    
    # Verify file integrity
    calculated_checksum = hashlib.sha256(content).hexdigest()
    if calculated_checksum != checksum:
        raise HTTPException(400, "File checksum mismatch")
    
    # Generate secure filename
    secure_name = f"{secrets.token_hex(16)}_{file.filename}"
    file_path = UPLOAD_DIR / secure_name
    
    # Save file securely
    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(content)
    
    return {
        "file_id": secrets.token_hex(16),
        "original_filename": file.filename,
        "secure_filename": secure_name,
        "checksum_verified": True,
        "user_id": user_id
    }

def validate_api_key(api_key: str, user_id: int) -> bool:
    """Validate API key for user (simplified)."""
    # In real implementation, check against database
    return len(api_key) >= 32
```

### Performance Optimization

#### **Streaming and Async Processing**
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

@app.post("/process-large-files/")
async def process_large_files(
    background_tasks: BackgroundTasks,
    data_file: Annotated[UploadFile, File()],
    config_file: Annotated[UploadFile, File()],
    processing_mode: Annotated[str, Form()],
    notification_email: Annotated[EmailStr, Form()],
    priority: Annotated[int, Form(ge=1, le=10)] = 5
):
    """Process large files asynchronously with configuration."""
    
    # Save files for processing
    data_path = UPLOAD_DIR / f"data_{secrets.token_hex(8)}.dat"
    config_path = UPLOAD_DIR / f"config_{secrets.token_hex(8)}.json"
    
    # Stream large file to disk
    async with aiofiles.open(data_path, 'wb') as f:
        while chunk := await data_file.read(8192):  # 8KB chunks
            await f.write(chunk)
    
    # Save config file
    config_content = await config_file.read()
    async with aiofiles.open(config_path, 'wb') as f:
        await f.write(config_content)
    
    # Schedule background processing
    job_id = secrets.token_hex(16)
    background_tasks.add_task(
        process_files_background,
        job_id, data_path, config_path, processing_mode, notification_email
    )
    
    return {
        "job_id": job_id,
        "status": "Processing started",
        "data_file": data_file.filename,
        "config_file": config_file.filename,
        "priority": priority,
        "notification_email": notification_email
    }

async def process_files_background(
    job_id: str, 
    data_path: Path, 
    config_path: Path, 
    mode: str, 
    email: str
):
    """Background file processing task."""
    try:
        # Simulate complex processing
        await asyncio.sleep(30)  # Replace with actual processing
        
        # Send completion notification
        send_notification(email, f"Job {job_id} completed successfully")
        
        # Cleanup temporary files
        data_path.unlink()
        config_path.unlink()
        
    except Exception as e:
        send_notification(email, f"Job {job_id} failed: {str(e)}")
```

### Key Learning Points
- **`Annotated` type hints improve code clarity** and separate type information from FastAPI metadata
- **Mixed form and file endpoints** enable rich data submission in single requests
- **Content-Type must be `multipart/form-data`** when combining files and form fields
- **File validation is essential** for security and data integrity
- **Form validation works with file uploads** using Pydantic validation patterns
- **Multiple files can be combined** with form data in sophisticated upload systems
- **Background processing** is recommended for large file operations
- **Security considerations** include API key validation, file integrity checks, and secure storage
- **Testing requires proper multipart** form data simulation with both files and form fields
- **Performance optimization** involves streaming large files and async processing

This lesson demonstrates how to build sophisticated upload systems that combine the flexibility of form data with the power of file uploads, enabling rich, interactive applications with comprehensive data submission capabilities!

---

## Lesson 17: Handling Errors

### Overview
- **Purpose**: Learn comprehensive error handling patterns in FastAPI applications
- **Key Concepts**: HTTP exceptions, custom exceptions, exception handlers, and error response formatting
- **Use Cases**: API error management, user-friendly error messages, debugging support, and robust application design

### File: `17HandlingErrors.py`

This lesson demonstrates various error handling techniques in FastAPI, from basic HTTP exceptions to sophisticated custom exception systems with dedicated handlers.

### Core Concepts

#### **HTTP Exception Basics**
```python
from fastapi import HTTPException

# Basic HTTP exception
if item_id not in items:
    raise HTTPException(status_code=404, detail="Item not found")
```

#### **HTTP Exception with Custom Headers**
```python
# Exception with additional headers
raise HTTPException(
    status_code=404, 
    detail="Item not found",
    headers={"X-Error": "There goes my error"}
)
```

#### **Custom Exception Classes**
```python
class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name
        super().__init__(f"Unicorn '{name}' caused an error")
```

### Implementation Details

#### **Basic Error Handling Endpoint**
```python
@app.get("/items/{item_id}")
async def read_item(item_id: str):
    """
    Retrieve an item by ID with basic error handling.
    
    This endpoint demonstrates basic HTTP exception handling in FastAPI.
    It retrieves an item from the sample data store and raises a 404 error
    if the item is not found.
    """
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}
```

#### **Error Handling with Custom Headers**
```python
@app.get("/items-header/{item_id}")
async def read_item_header(item_id: str):
    """
    Retrieve an item by ID with custom headers in error responses.
    
    This endpoint demonstrates how to include custom headers in HTTP exception
    responses. It's useful for providing additional metadata or debugging
    information in error responses.
    """
    if item_id not in items:
        raise HTTPException(
            status_code=404, 
            detail="Item not found",
            headers={"X-Error": "There goes my error"}
        )
    return {"item": items[item_id]}
```

#### **Custom Exception Handler**
```python
@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    """
    Custom exception handler for UnicornException.
    
    This function demonstrates how to create custom exception handlers in FastAPI
    that provide specific handling for custom exception types.
    """
    return JSONResponse(
        status_code=418,
        content={"message": f"The '{exc.name}' caused an error!"},
    )
```

### Error Handling Patterns

#### **HTTP Status Code Guidelines**

| Status Code | Use Case | Example |
|-------------|----------|---------|
| **400 Bad Request** | Invalid input data | Missing required fields |
| **401 Unauthorized** | Authentication required | Invalid API key |
| **403 Forbidden** | Permission denied | Insufficient privileges |
| **404 Not Found** | Resource doesn't exist | Item ID not found |
| **409 Conflict** | Resource conflict | Duplicate email address |
| **422 Unprocessable Entity** | Validation errors | Invalid email format |
| **429 Too Many Requests** | Rate limiting | API quota exceeded |
| **500 Internal Server Error** | Server errors | Database connection failed |

#### **Comprehensive Error Handling Example**
```python
from enum import Enum
from typing import Optional

class ErrorCode(str, Enum):
    ITEM_NOT_FOUND = "ITEM_NOT_FOUND"
    INVALID_INPUT = "INVALID_INPUT"
    PERMISSION_DENIED = "PERMISSION_DENIED"

class APIError(Exception):
    def __init__(
        self, 
        message: str, 
        error_code: ErrorCode, 
        status_code: int = 400,
        headers: Optional[dict] = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.headers = headers or {}
        super().__init__(message)

@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    return JSONResponse(
        status_code=exc.status_code,
        headers=exc.headers,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "timestamp": datetime.now().isoformat(),
                "path": str(request.url)
            }
        }
    )

@app.get("/items/{item_id}")
async def get_item_with_detailed_errors(item_id: str):
    if not item_id:
        raise APIError(
            message="Item ID is required",
            error_code=ErrorCode.INVALID_INPUT,
            status_code=400
        )
    
    if item_id not in items:
        raise APIError(
            message=f"Item with ID '{item_id}' was not found",
            error_code=ErrorCode.ITEM_NOT_FOUND,
            status_code=404
        )
    
    return {"item": items[item_id]}
```

### Advanced Error Handling Techniques

#### **Validation Error Customization**
```python
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Custom handler for Pydantic validation errors."""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation failed",
            "details": errors,
            "timestamp": datetime.now().isoformat()
        }
    )
```

#### **Global Exception Handler**
```python
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global handler for unexpected exceptions."""
    
    # Log the error for debugging
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    
    # Don't expose internal error details in production
    if app.debug:
        error_detail = str(exc)
    else:
        error_detail = "An internal server error occurred"
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": error_detail,
            "timestamp": datetime.now().isoformat()
        }
    )
```

#### **Error Logging and Monitoring**
```python
import logging
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoggedHTTPException(HTTPException):
    """HTTPException that automatically logs errors."""
    
    def __init__(self, status_code: int, detail: str, **kwargs):
        super().__init__(status_code, detail, **kwargs)
        logger.error(f"HTTP {status_code}: {detail}")

@app.get("/items/{item_id}/logged")
async def get_item_with_logging(item_id: str):
    """Endpoint with automatic error logging."""
    if item_id not in items:
        raise LoggedHTTPException(
            status_code=404,
            detail=f"Item '{item_id}' not found"
        )
    
    logger.info(f"Successfully retrieved item: {item_id}")
    return {"item": items[item_id]}
```

### Error Response Formats

#### **Standard Error Response**
```json
{
    "detail": "Item not found"
}
```

#### **Detailed Error Response**
```json
{
    "error": {
        "code": "ITEM_NOT_FOUND",
        "message": "Item with ID 'xyz' was not found",
        "timestamp": "2025-10-28T10:30:00Z",
        "path": "/items/xyz"
    }
}
```

#### **Validation Error Response**
```json
{
    "error": "Validation failed",
    "details": [
        {
            "field": "email",
            "message": "field required",
            "type": "value_error.missing"
        },
        {
            "field": "age",
            "message": "ensure this value is greater than 0",
            "type": "value_error.number.not_gt"
        }
    ],
    "timestamp": "2025-10-28T10:30:00Z"
}
```

### Testing Error Handling

#### **Testing HTTP Exceptions**
```python
from fastapi.testclient import TestClient

def test_item_not_found():
    client = TestClient(app)
    response = client.get("/items/nonexistent")
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

def test_item_not_found_with_headers():
    client = TestClient(app)
    response = client.get("/items-header/nonexistent")
    
    assert response.status_code == 404
    assert response.headers["X-Error"] == "There goes my error"
    assert response.json() == {"detail": "Item not found"}
```

#### **Testing Custom Exceptions**
```python
def test_unicorn_exception():
    client = TestClient(app)
    response = client.get("/unicorns/yolo")
    
    assert response.status_code == 418
    assert response.json() == {"message": "The 'yolo' caused an error!"}

def test_unicorn_success():
    client = TestClient(app)
    response = client.get("/unicorns/sparkles")
    
    assert response.status_code == 200
    assert response.json() == {"unicorn_name": "sparkles"}
```

#### **Testing Validation Errors**
```python
def test_validation_error():
    client = TestClient(app)
    response = client.post("/users/", json={"name": ""})  # Invalid data
    
    assert response.status_code == 422
    assert "validation" in response.json()["error"].lower()
```

### Error Handling Best Practices

#### **Security Considerations**
```python
@app.exception_handler(Exception)
async def secure_exception_handler(request: Request, exc: Exception):
    """Secure exception handler that doesn't leak sensitive information."""
    
    # Log full error details for debugging
    logger.error(f"Error on {request.url}: {exc}", exc_info=True)
    
    # Determine what to expose to client
    if isinstance(exc, HTTPException):
        # HTTPException details are safe to expose
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )
    elif isinstance(exc, RequestValidationError):
        # Validation errors are safe to expose
        return JSONResponse(
            status_code=422,
            content={"detail": "Validation error", "errors": exc.errors()}
        )
    else:
        # Don't expose internal error details
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )
```

#### **Rate Limiting with Error Handling**
```python
from time import time
from collections import defaultdict

# Simple rate limiting (use Redis in production)
request_counts = defaultdict(list)

class RateLimitExceeded(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=429,
            detail="Rate limit exceeded",
            headers={"Retry-After": "60"}
        )

def check_rate_limit(client_id: str, limit: int = 100, window: int = 3600):
    """Check if client has exceeded rate limit."""
    now = time()
    client_requests = request_counts[client_id]
    
    # Remove old requests outside the window
    client_requests[:] = [req_time for req_time in client_requests if now - req_time < window]
    
    if len(client_requests) >= limit:
        raise RateLimitExceeded()
    
    client_requests.append(now)

@app.get("/rate-limited-items/{item_id}")
async def get_item_with_rate_limit(item_id: str, request: Request):
    """Endpoint with rate limiting."""
    client_ip = request.client.host
    check_rate_limit(client_ip)
    
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return {"item": items[item_id]}
```

### Production Error Handling

#### **Health Check Endpoints**
```python
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    try:
        # Check database connection, external services, etc.
        # This is a simplified example
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail="Service temporarily unavailable"
        )
```

#### **Error Metrics and Monitoring**
```python
from prometheus_client import Counter, Histogram

# Metrics for monitoring
error_counter = Counter('http_errors_total', 'Total HTTP errors', ['status_code', 'endpoint'])
response_time = Histogram('http_request_duration_seconds', 'Request duration')

@app.middleware("http")
async def error_monitoring_middleware(request: Request, call_next):
    """Middleware to collect error metrics."""
    start_time = time()
    
    try:
        response = await call_next(request)
        
        # Record metrics
        if response.status_code >= 400:
            error_counter.labels(
                status_code=response.status_code,
                endpoint=request.url.path
            ).inc()
        
        response_time.observe(time() - start_time)
        return response
        
    except Exception as e:
        # Record unhandled errors
        error_counter.labels(status_code=500, endpoint=request.url.path).inc()
        response_time.observe(time() - start_time)
        raise
```

### Real-World Error Scenarios

#### **Database Connection Errors**
```python
from sqlalchemy.exc import SQLAlchemyError

@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handle database-related errors."""
    logger.error(f"Database error: {exc}")
    
    return JSONResponse(
        status_code=503,
        content={
            "error": "Database temporarily unavailable",
            "message": "Please try again later",
            "timestamp": datetime.now().isoformat()
        }
    )
```

#### **External API Errors**
```python
import httpx

class ExternalAPIError(Exception):
    def __init__(self, service: str, status_code: int, message: str):
        self.service = service
        self.status_code = status_code
        self.message = message
        super().__init__(f"{service} API error: {message}")

@app.exception_handler(ExternalAPIError)
async def external_api_error_handler(request: Request, exc: ExternalAPIError):
    """Handle external API errors."""
    return JSONResponse(
        status_code=502,
        content={
            "error": f"{exc.service} service unavailable",
            "message": "External service is temporarily down",
            "timestamp": datetime.now().isoformat()
        }
    )

@app.get("/external-data/{item_id}")
async def get_external_data(item_id: str):
    """Endpoint that calls external API with error handling."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://api.example.com/items/{item_id}")
            
            if response.status_code != 200:
                raise ExternalAPIError(
                    service="Example API",
                    status_code=response.status_code,
                    message=response.text
                )
            
            return response.json()
            
    except httpx.RequestError as e:
        raise ExternalAPIError(
            service="Example API",
            status_code=0,
            message=f"Connection error: {str(e)}"
        )
```

### Key Learning Points
- **HTTPException is the standard way** to raise HTTP errors in FastAPI
- **Custom headers in exceptions** provide additional context for debugging
- **Custom exception classes** enable domain-specific error handling
- **Exception handlers** provide consistent error response formatting
- **Proper HTTP status codes** improve API usability and client integration
- **Error logging is crucial** for debugging and monitoring
- **Security considerations** require careful handling of error details
- **Rate limiting and monitoring** help prevent abuse and track performance
- **Validation error customization** improves user experience
- **Global exception handlers** catch unexpected errors gracefully

This lesson establishes robust error handling patterns that improve API reliability, user experience, and maintainability while providing proper debugging support for developers!
