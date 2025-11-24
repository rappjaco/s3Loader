from fastapi import FastAPI, File, Form, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from upload import write_file_shared_storage, list_bucket_files
from scanner import Scanner

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
