from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# TODO: Mount the static files directory
# Use app.mount() to serve files from the "static" directory at the "/static" path
# Hint: app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    # TODO: Return information about the static files demo
    # Include links to the static demo page
    return {
        "message": "Welcome to the Static Files Demo!",
        "static_files_url": "/static/index.html"
    }
