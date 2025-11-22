from fastapi import FastAPI, File, Form, UploadFile, BackgroundTasks
from pydantic import BaseModel
from upload import write_file_shared_storage, list_bucket_files
from scanner import Scanner

app = FastAPI()

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
