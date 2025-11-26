from fastapi import FastAPI, File, Form, UploadFile, BackgroundTasks
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from upload import write_file_shared_storage, list_bucket_files
from scanner import Scanner
from auth import github_oauth_redirect, github_token_resolve

REDIRECT_URI= "http://localhost:8000"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# class File(BaseModel):
#     dest_file_name: str
#     file: 


@app.get("/api/v1/list")
async def list_files():
    return list_bucket_files()

@app.post("/api/v1/upload")
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(),    
):  
    contents = await file.read()
    result = write_file_shared_storage(contents, file.filename)
    scanner = Scanner(file.filename)
    background_tasks.add_task(scanner.scanner_init)
    return {
        "response": result
    }

@app.get("/api/v1/login")
async def login(code: str | None = None ):

    if (code):
        response = github_token_resolve(code)
        print(response)
        if (response.get("access_token")):
            redirect = RedirectResponse(url="http://localhost:3000/")
            redirect.set_cookie(
                key="session_id",
                value=response["access_token"],
                secure=False
            )
            return redirect
        else:
           raise ValueError("No Access Token") 
            
    else:
        return github_oauth_redirect()