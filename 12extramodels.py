"""
Extra Models - Multiple Related Models for Different Use Cases

This module demonstrates how to create multiple related Pydantic models for different
purposes in a FastAPI application. It showcases the common pattern of having separate
models for input, output, and database storage, enabling better security, data separation,
and API design.

Key concepts covered:
- Model inheritance with BaseModel and Pydantic
- Separating input, output, and database models
- Password handling and security practices
- Response model filtering
- Model composition and data transformation
- Using model_dump() for data conversion

Design Pattern:
- UserBase: Common fields shared across all user models
- UserIn: Input model with password (for API requests)
- UserOut: Output model without password (for API responses)
- UserInDB: Database model with hashed password (for storage)

This pattern ensures:
1. Passwords are never returned in API responses
2. Raw passwords are never stored in the database
3. Clear separation of concerns between different data representations
4. Type safety throughout the application flow
"""

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()

#Create three user models:
# 1. UserIn - for input data (includes password)
# 2. UserOut - for output data (excludes password)  
# 3. UserInDB - for database storage (includes hashed_password)
class Userbase(BaseModel):
    """
    Base user model containing common fields shared across all user models.
    
    This base class defines the core user attributes that are consistent
    across input, output, and database representations. Using inheritance
    promotes code reuse and ensures consistency.
    
    Attributes:
        username (str): Unique username for the user
        email (EmailStr): Valid email address with automatic validation
    
    Note:
        EmailStr requires the 'email-validator' package for validation
    """
    username: str
    email: EmailStr
    
class UserIn(Userbase):
    """
    Input model for user creation requests.
    
    This model extends UserBase to include the raw password field, which is
    needed when creating a new user account. The password will be hashed
    before storage and never returned in API responses.
    
    Attributes:
        username (str): Inherited from UserBase
        email (EmailStr): Inherited from UserBase
        password (str): Raw password provided by the user
    
    Example:
        {
            "username": "johndoe",
            "email": "johndoe@example.com",
            "password": "secretpassword123"
        }
    """
    password: str
    
class UserOut(Userbase):
    """
    Output model for user data in API responses.
    
    This model excludes sensitive information like passwords and is used
    as the response_model for API endpoints. It ensures that passwords
    are never accidentally exposed in API responses.
    
    Attributes:
        username (str): Inherited from UserBase
        email (EmailStr): Inherited from UserBase
    
    Note:
        No password field - this model is safe for public API responses
    
    Example:
        {
            "username": "johndoe",
            "email": "johndoe@example.com"
        }
    """
    pass

class UserInDB(Userbase):
    """
    Database model for user storage.
    
    This model extends UserBase to include the hashed password field,
    which is stored in the database instead of the raw password. This
    ensures secure password storage.
    
    Attributes:
        username (str): Inherited from UserBase
        email (EmailStr): Inherited from UserBase
        hashed_password (str): Securely hashed version of the user's password
    
    Example:
        {
            "username": "johndoe",
            "email": "johndoe@example.com",
            "hashed_password": "supersecretpassword123"
        }
    """
    hashed_password: str

# Create a fake password hasher function
# async def fake_password_hasher(raw_password: str):
#     return "supersecret" + raw_password
async def fake_password_hasher(raw_password: str) -> str:
    """
    Simulate password hashing for demonstration purposes.
    
    In a real application, this would use a proper cryptographic hashing
    function like bcrypt, scrypt, or Argon2. This function simply prepends
    a string to demonstrate the concept of password transformation.
    
    Args:
        raw_password (str): The plain text password from user input
        
    Returns:
        str: A "hashed" password (in reality just prefixed with a string)
    
    Note:
        This is NOT secure! In production, use proper password hashing:
        - bcrypt: `bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())`
        - Argon2: `argon2.PasswordHasher().hash(password)`
        - Never store plain text passwords
    
    Example:
        >>> await fake_password_hasher("mypassword")
        "supersecretmypassword"
    """
    return "supersecret" + raw_password

# Create a fake save user function that:
# - Takes a UserIn object
# - Hashes the password (remember to await the hasher!)
# - Creates a UserInDB object with the hashed password
# - Returns the UserInDB object
# async def fake_save_user(user_in: UserIn):
#     hashed_password = await fake_password_hasher(user_in.password)
#     user_in_db = UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
#     print("User saved! ..not really")
#     return user_in_db

async def fake_save_user(user_in: UserIn) -> UserInDB:
    """
    Simulate saving a user to the database with password hashing.
    
    This function demonstrates the typical flow of processing user input:
    1. Extract the raw password from input data
    2. Hash the password using a secure hashing function
    3. Create a database model with the hashed password
    4. Save to database (simulated here)
    
    The function uses Pydantic's model_dump() to convert the input model
    to a dictionary, then unpacks it while adding the hashed password.
    
    Args:
        user_in (UserIn): The input user data including raw password
        
    Returns:
        UserInDB: The user data prepared for database storage with hashed password
    
    Process Flow:
        UserIn (with password) → hash password → UserInDB (with hashed_password)
    
    Example:
        >>> user_input = UserIn(username="john", email="john@example.com", password="secret")
        >>> user_db = await fake_save_user(user_input)
        >>> user_db.hashed_password
        "supersecretsecret"
    
    Note:
        In a real application, this would:
        - Use proper password hashing (bcrypt, Argon2, etc.)
        - Actually save to a database
        - Handle potential database errors
        - Validate uniqueness constraints
    """
    hashed_password = await fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db

# Create a POST endpoint at "/user/" that:
# - Accepts UserIn data
# - Uses response_model=UserOut to filter the response
# - Calls fake_save_user and returns the result (remember to await it!)
# @app.post("/user/", response_model=UserOut)
# async def create_user(user_in: UserIn):
#     user_saved = await fake_save_user(user_in)
#     return user_saved

@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn) -> UserOut:
    """
    Create a new user account.
    
    This endpoint demonstrates the complete flow of user creation using
    multiple related models. It accepts user input with a password,
    processes and stores the data securely, then returns safe output data.
    
    The endpoint showcases several important patterns:
    1. Input validation using UserIn model
    2. Password hashing for security
    3. Database storage preparation with UserInDB model
    4. Response filtering using UserOut model
    5. Automatic password exclusion from responses
    
    Args:
        user_in (UserIn): The input user data including raw password
        
    Returns:
        UserOut: The created user data excluding the password
    
    Response Model:
        The response_model=UserOut parameter ensures that:
        - Only safe fields (username, email) are returned
        - Password and hashed_password are automatically excluded
        - Response matches the UserOut model structure
        
    Security Features:
        - Raw passwords are never stored
        - Passwords are automatically excluded from responses
        - Email validation ensures proper format
        
    Example Request:
        POST /user/
        Content-Type: application/json
        
        {
            "username": "johndoe",
            "email": "johndoe@example.com",
            "password": "supersecret123"
        }
    
    Example Response:
        HTTP 200 OK
        Content-Type: application/json
        
        {
            "username": "johndoe",
            "email": "johndoe@example.com"
        }
    
    HTTP Status Codes:
        - 200: User created successfully
        - 422: Validation error (invalid email format, missing fields, etc.)
    
    Note:
        Even though fake_save_user returns a UserInDB object (which contains
        hashed_password), the response_model=UserOut ensures only username
        and email are included in the API response.
    """
    user_saved = await fake_save_user(user_in)
    return user_saved