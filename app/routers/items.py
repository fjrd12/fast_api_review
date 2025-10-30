# Import the necessary FastAPI components
# Hint: You need APIRouter, Depends, and HTTPException
from fastapi import APIRouter, Depends, HTTPException

# mport the dependency from the parent package
# Hint: Use relative import ..dependencies to go up one level
from ..dependencies import get_token_header

# TODO: Create an APIRouter with configuration
# Hint: Set prefix="/items", tags=["items"], dependencies=[Depends(get_token_header)], 
# and responses={404: {"description": "Not found"}}
router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


# Sample items database
fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


# Create a GET endpoint for "/" that returns all items
@router.get("/")
async def read_items():
    return fake_items_db


# Create a GET endpoint for "/{item_id}" that returns a specific item
# If item not found, raise HTTPException with status_code=404 and detail="Item not found"
@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}


# Create a PUT endpoint for "/{item_id}" with custom tags and responses
# It should only allow updating "plumbus", otherwise raise 403 error
@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}
