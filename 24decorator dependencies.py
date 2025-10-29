from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()

# Create verify_token dependency that checks X-Token header
# Should raise HTTPException(status_code=400) if token != "fake-super-secret-token"
async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")    

# Create verify_key dependency that checks X-Key header  
# Should raise HTTPException(status_code=400) if key != "fake-super-secret-key"
# Should return the key value

async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


# TODO: Create GET /items/ endpoint with both verify_token and verify_key in dependencies parameter
# Use: dependencies=[Depends(verify_token), Depends(verify_key)]
# Return: [{"item": "Foo"}, {"item": "Bar"}]
@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():    
    return [{"item": "Foo"}, {"item": "Bar"}]
    