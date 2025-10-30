# Import the necessary modules
# Hint: You need FastAPI, Depends, and the modules we created
from fastapi import FastAPI, Depends

# Import dependencies from our dependencies module
from .dependencies import get_query_token, get_token_header

# Import routers from our routers package
from .routers import items, users

# Import admin router from internal package
from .internal import admin

# Create FastAPI app with global dependencies
# Hint: Use dependencies=[Depends(get_query_token)] to apply to all routes
app = FastAPI(dependencies=[Depends(get_query_token)])

# Include the users router
app.include_router(users.router)

# Include the items router
app.include_router(items.router)

# Include the admin router with configuration
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
