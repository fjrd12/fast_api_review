# Import APIRouter from FastAPI
from fastapi import APIRouter

# Create an APIRouter instance
router = APIRouter()


# Create a POST endpoint for "/" that handles admin operations
@router.post("/")
async def update_admin():
    return {"message": "Admin getting schwifty"}
