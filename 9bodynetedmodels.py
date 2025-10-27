"""
FastAPI Body Nested Models - Complex Data Structures

This module demonstrates how to create and handle complex nested data structures
using FastAPI and Pydantic. It covers nested models, lists of models, sets,
dictionaries, and various collection types for building sophisticated APIs.

Key concepts covered:
- Nested Pydantic models (models within models)
- Lists of nested models for collections
- Sets for unique value collections
- Dictionary types with specific key/value constraints
- HttpUrl validation for URL fields
- Complex data structure validation
- Real-world API patterns with nested data

Run with: fastapi dev 9bodynetedmodels.py
"""

from typing import Dict, List, Set, Union
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI(
    title="Nested Models Demo",
    description="A FastAPI application demonstrating complex nested data structures with Pydantic",
    version="1.0.0"
)


class Image(BaseModel):
    """
    Nested Pydantic model representing an image resource.
    
    This model demonstrates basic nested model concepts with URL validation.
    It's designed to be embedded within other models to represent image data.
    
    Attributes:
        url (HttpUrl): The URL of the image (validated as proper URL format)
        name (str): The display name or title of the image
        
    Example:
        {
            "url": "https://example.com/image.jpg",
            "name": "Product Image"
        }
        
    Validation:
        - url: Must be a valid HTTP/HTTPS URL format
        - name: Required string field
    """
    url: HttpUrl
    name: str


class Item(BaseModel):
    """
    Main item model with nested structures and collections.
    
    This model demonstrates various nested data patterns including:
    - Optional nested models (single image)
    - Sets for unique collections (tags)
    - Union types for optional fields
    
    Attributes:
        name (str): The name of the item (required)
        description (Union[str, None]): Optional description of the item
        price (float): The price of the item (required)
        tax (Union[float, None]): Optional tax amount
        tags (Set[str]): Set of unique string tags (no duplicates allowed)
        image (Union[Image, None]): Optional single nested Image model
        
    Example:
        {
            "name": "Gaming Laptop",
            "description": "High-performance gaming laptop",
            "price": 1299.99,
            "tax": 130.00,
            "tags": ["electronics", "gaming", "computers"],
            "image": {
                "url": "https://example.com/laptop.jpg",
                "name": "Laptop Photo"
            }
        }
        
    Collection Features:
        - tags: Set automatically removes duplicates
        - image: Can be null/omitted entirely
        - Nested validation: Image model validated if provided
    """
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()
    image: Union[Image, None] = None


class ItemWithImages(BaseModel):
    """
    Item model with multiple images support.
    
    This model extends the basic item concept to support multiple images,
    demonstrating lists of nested models - a common pattern for APIs
    that need to handle collections of related objects.
    
    Attributes:
        name (str): The name of the item (required)
        description (Union[str, None]): Optional description of the item
        price (float): The price of the item (required)
        tax (Union[float, None]): Optional tax amount
        tags (Set[str]): Set of unique string tags
        images (List[Image]): List of Image models (can be empty)
        
    Example:
        {
            "name": "Gaming Setup",
            "description": "Complete gaming setup with multiple components",
            "price": 2499.99,
            "tax": 250.00,
            "tags": ["gaming", "electronics", "bundle"],
            "images": [
                {
                    "url": "https://example.com/setup1.jpg",
                    "name": "Main Setup"
                },
                {
                    "url": "https://example.com/setup2.jpg",
                    "name": "Side View"
                }
            ]
        }
        
    List Features:
        - images: Can contain 0 or more Image objects
        - Order preservation: List maintains image order
        - Individual validation: Each Image in list is validated
        - Empty list allowed: Default is empty list []
    """
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()
    images: List[Image] = []


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item) -> dict:
    """
    Update an item with nested model support.
    
    This endpoint demonstrates handling nested models in request bodies.
    It accepts an Item model which can contain an optional nested Image model,
    showcasing how FastAPI automatically validates complex nested structures.
    
    Args:
        item_id (int): The ID of the item to update (path parameter)
        item (Item): Item data with optional nested image (request body)
        
    Returns:
        dict: Dictionary containing item_id and the complete item data
        
    Request Body Example:
        {
            "name": "Gaming Mouse",
            "description": "RGB gaming mouse with 12 buttons",
            "price": 79.99,
            "tax": 8.00,
            "tags": ["gaming", "mouse", "rgb"],
            "image": {
                "url": "https://example.com/mouse.jpg",
                "name": "Gaming Mouse Photo"
            }
        }
        
    Response Example:
        {
            "item_id": 123,
            "item": {
                "name": "Gaming Mouse",
                "description": "RGB gaming mouse with 12 buttons",
                "price": 79.99,
                "tax": 8.0,
                "tags": ["gaming", "mouse", "rgb"],
                "image": {
                    "url": "https://example.com/mouse.jpg",
                    "name": "Gaming Mouse Photo"
                }
            }
        }
        
    Validation Features:
        - Nested model validation: Image model validated if provided
        - Set deduplication: Duplicate tags automatically removed
        - URL validation: Image URL must be valid HTTP/HTTPS format
        - Optional nesting: Image can be omitted entirely
        
    Error Cases (422):
        - Invalid URL format in image.url
        - Missing required fields (name, price)
        - Invalid data types for any field
    """
    return {"item_id": item_id, "item": item}


@app.put("/items/{item_id}/images")
async def update_item_with_images(item_id: int, item: ItemWithImages) -> dict:
    """
    Update an item with multiple images support.
    
    This endpoint demonstrates handling lists of nested models in request bodies.
    It showcases how FastAPI validates arrays of complex objects, making it
    perfect for scenarios where items can have multiple associated images.
    
    Args:
        item_id (int): The ID of the item to update (path parameter)
        item (ItemWithImages): Item data with list of images (request body)
        
    Returns:
        dict: Dictionary containing item_id and the complete item data with images
        
    Request Body Example:
        {
            "name": "Gaming Setup Bundle",
            "description": "Complete gaming setup with monitor, keyboard, mouse",
            "price": 1899.99,
            "tax": 190.00,
            "tags": ["gaming", "bundle", "complete-setup"],
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
                    "url": "https://example.com/setup-detail.jpg",
                    "name": "Detail Shot"
                }
            ]
        }
        
    Response Example:
        {
            "item_id": 456,
            "item": {
                "name": "Gaming Setup Bundle",
                "description": "Complete gaming setup with monitor, keyboard, mouse",
                "price": 1899.99,
                "tax": 190.0,
                "tags": ["gaming", "bundle", "complete-setup"],
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
                        "url": "https://example.com/setup-detail.jpg",
                        "name": "Detail Shot"
                    }
                ]
            }
        }
        
    List Validation Features:
        - Each image in list individually validated
        - Order preservation: Images maintain their order
        - Empty list allowed: Can send empty images array
        - URL validation: Each image URL validated separately
        - Duplicate URLs allowed: Same URL can appear in multiple images
        
    Use Cases:
        - Product galleries with multiple photos
        - Documentation with multiple screenshots
        - Real estate listings with multiple property images
        - Social media posts with multiple attachments
    """
    return {"item_id": item_id, "item": item}


@app.post("/index-weights/")
async def create_index_weights(weights: Dict[int, float]) -> dict:
    """
    Create index weights using dictionary types.
    
    This endpoint demonstrates handling dictionary types in request bodies,
    where the structure is a mapping of specific key types to value types.
    Perfect for scenarios like search rankings, item weights, or any key-value mappings.
    
    Args:
        weights (Dict[int, float]): Dictionary mapping integer indices to float weights
        
    Returns:
        dict: Dictionary containing the received weights
        
    Request Body Example:
        {
            "1": 0.8,
            "2": 1.2,
            "5": 0.5,
            "10": 2.0,
            "15": 1.5
        }
        
    Response Example:
        {
            "weights": {
                "1": 0.8,
                "2": 1.2,
                "5": 0.5,
                "10": 2.0,
                "15": 1.5
            }
        }
        
    Dictionary Validation:
        - Keys: Must be convertible to integers
        - Values: Must be valid float numbers
        - Structure: Flexible number of key-value pairs
        - Type enforcement: Automatic conversion and validation
        
    Use Cases:
        - Search result rankings and weights
        - Item priority or importance scores
        - Configuration parameters with numeric IDs
        - Statistical data with indexed values
        - Performance metrics by category ID
        
    Validation Examples:
        Valid:
        - {"1": 1.0, "2": 2.5} ✓
        - {"0": 0.0, "999": 10.5} ✓
        - {} ✓ (empty dict allowed)
        
        Invalid (422 errors):
        - {"abc": 1.0} ✗ (key not convertible to int)
        - {"1": "not_a_number"} ✗ (value not convertible to float)
        - {"1.5": 1.0} ✗ (key not a valid integer)
        
    Note:
        JSON automatically converts number keys to strings during transmission,
        but Pydantic converts them back to integers for validation.
    """
    return {"weights": weights}
