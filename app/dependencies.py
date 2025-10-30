# Import the necessary FastAPI components
# Hint: You need Header and HTTPException
from fastapi import Header, HTTPException


# Create a dependency that validates the X-Token header
async def get_token_header(x_token: str = Header()):
    # Check if x_token equals "fake-super-secret-token"
    # If not, raise HTTPException with status_code=400 and detail="X-Token header invalid"
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


# Create a dependency that validates the query token
async def get_query_token(token: str):
    # Check if token equals "jessica"
    # If not, raise HTTPException with status_code=400 and detail="No Jessica token provided"
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")
