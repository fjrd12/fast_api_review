from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Annotated

app = FastAPI()

# Pydantic model
class Item(BaseModel):
    name: str
    price: float

# Simple in-memory database
items_db: Dict[int, Item] = {}
next_id = 1

# Simulated database session class (like in real applications)
class DBSession:
    def __init__(self):
        self.connected = True
        self.transaction_count = 0
        print("Database connection established")
    
    def close(self):
        self.connected = False
        print("Database connection closed")

# TODO: Create a database session dependency with yield
# Follow the official FastAPI pattern from the docs:
# 
async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()
#
# This ensures the database session is always closed after the request

async def get_db():
    # TODO: Implement the database session dependency with yield
    # 1. Create a DBSession instance
    # 2. Use try/yield/finally pattern
    # 3. Yield the session for injection
    # 4. Close the session in finally block
        db = DBSession()
        try:
            yield db
        finally:
            db.close()

# TODO: Create endpoints that use the database dependency

# POST /items/ - Create a new item
# - Use: item: Item, db: Annotated[DBSession, Depends(get_db)]
# - Increment db.transaction_count
# - Store item in items_db with next_id
# - Return the item with its ID
@app.post("/items/")
async def create_item(item: Item, db: Annotated[DBSession, Depends(get_db)]) -> Dict:
    global next_id
    db.transaction_count += 1
    item_id = next_id
    items_db[item_id] = item
    next_id += 1
    return {"id": item_id, **item.model_dump()}

# GET /items/ - Get all items
# - Use: db: Annotated[DBSession, Depends(get_db)]
# - Increment db.transaction_count  
# - Return all items from items_db
@app.get("/items/")
async def get_items(db: Annotated[DBSession, Depends(get_db)]) -> Dict[int, Item]:
    db.transaction_count += 1
    return items_db

print("🚀 Ready to implement dependencies with yield!")
print("💡 The DBSession class is provided - focus on the yield pattern!")