# Response Status Code
# Learn how to specify HTTP status codes for your API responses

from fastapi import FastAPI
from fastapi import status

app = FastAPI()

# Create a POST endpoint at "/items/" that:
# 1. Accepts a "name" parameter as a query parameter (string)
# 2. Returns a dictionary with the name
# 3. Uses status code 201 (Created) instead of the default 200
# Hint: Use the status_code parameter in the decorator
# Example: @app.post("/items/", status_code=???)
# For query parameters, just define: def create_item(name: str):
# Hint: from fastapi import status
# Then use: status.HTTP_201_CREATED

@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}


