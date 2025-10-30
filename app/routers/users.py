#Import APIRouter from FastAPI
from fastapi import APIRouter

# Create an APIRouter instance
router = APIRouter()


# Create a GET endpoint for "/users/" with tags=["users"]
# It should return a list of users: [{"username": "Rick"}, {"username": "Morty"}]
@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


# Create a GET endpoint for "/users/me" with tags=["users"]
# It should return the current user: {"username": "fakecurrentuser"}
@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


# Create a GET endpoint for "/users/{username}" with tags=["users"]
# It should accept a username parameter and return: {"username": username}
@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
