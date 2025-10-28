# Request Forms
# Learn how to receive form data instead of JSON

from fastapi import FastAPI, Form

app = FastAPI()

# TODO: Import Form from fastapi
# Hint: from fastapi import FastAPI, Form

# TODO: Create a POST endpoint at "/login/" that:
# 1. Accepts "username" and "password" as form fields (not JSON)
# 2. Returns a dictionary with the username
# 
# Hint: Use Form() as the default value for parameters
# Example: username: str = Form(), password: str = Form()
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