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
