from typing import Annotated

from fastapi import FastAPI, File, Form, UploadFile

app = FastAPI()

# TODO: Create an endpoint that accepts both files and form data
# The endpoint should:
# 1. Accept a 'file' parameter as bytes using File()
# 2. Accept a 'fileb' parameter as UploadFile using File()  
# 3. Accept a 'token' parameter as string using Form()
# 4. Use Annotated type hints for all parameters
# 5. Return file_size, token, and fileb_content_type

@app.post("/files/")
async def create_file(
    file: Annotated[bytes, File()],
    fileb: Annotated[UploadFile, File()],
    token: Annotated[str, Form()]
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type
    }