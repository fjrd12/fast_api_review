# Request Files
# Learn how to handle file uploads in FastAPI

from fastapi import FastAPI, File, UploadFile

app = FastAPI()

# TODO: Import File and UploadFile from fastapi
# Hint: from fastapi import FastAPI, File, UploadFile

# TODO: Create a POST endpoint at "/files/" that:
# 1. Accepts a file parameter as bytes using File()
# 2. Returns the file size in a dictionary
# 
# Hint: Use file: bytes = File() for the parameter
# Return: {"file_size": len(file)}
@app.post("/files/")
async def create_file(file: bytes = File()):
    """
    Upload a file and return its size.
    
    This endpoint demonstrates how to handle file uploads in FastAPI using
    the File class. The uploaded file is read as bytes, and the size of
    the file is returned in the response.
    
    Args:
        file (bytes): The uploaded file content as bytes
        
    Returns:
        dict: A dictionary containing the size of the uploaded file in bytes
        
    Example Request:
        POST /files/
        Content-Type: multipart/form-data
        file: <file to upload>
        
    Example Response:
        {
            "file_size": 12345
        }
        
    Note:
        - The File() function is used to declare that the parameter should
          be interpreted as a file upload.
        - The uploaded file is read into memory as bytes, which may not be
          suitable for very large files.
    """
    return {"file_size": len(file)}

# Create a POST endpoint at "/uploadfile/" that:
# 1. Accepts a file parameter as UploadFile
# 2. Returns the filename in a dictionary
#
# Hint: Use file: UploadFile for the parameter (no = File() needed)
# Return: {"filename": file.filename}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    """
    Upload a file and return its filename.
    
    This endpoint demonstrates how to handle file uploads in FastAPI using
    the UploadFile class. The uploaded file is represented as an UploadFile
    object, which provides access to metadata such as the filename.
    
    Args:
        file (UploadFile): The uploaded file as an UploadFile object
        
    Returns:
        dict: A dictionary containing the filename of the uploaded file
        
    Example Request:
        POST /uploadfile/
        Content-Type: multipart/form-data
        file: <file to upload>
        
    Example Response:
        {
            "filename": "example.txt"
        }
        
    Note:
        - The UploadFile class is more efficient for handling large files
          compared to reading the entire file into memory as bytes.
        - You can access additional metadata and methods on the UploadFile
          object, such as content_type and file.read().
    """
    return {"filename": file.filename}