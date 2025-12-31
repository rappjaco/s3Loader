from fastapi import FastAPI, File, UploadFile, BackgroundTasks, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from backend_upload import write_file_shared_storage, list_bucket_files
from backend_scanner import Scanner
from pydantic import BaseModel
from backend_auth import oauth_redirect, token_resolve, auth_user_data, validate_user_token, LoginHandler
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Annotated

REDIRECT_URI = "http://localhost:8000"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TokenData(BaseModel):
    user_access_token: str


#engine = create_engine("postgresql://scanner:scanner_dev_password@localhost:5432/scanner")
engine = create_engine("sqlite:///./sqlite.db")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)



@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/api/v1/list")
async def list_files(user_token: str = Depends(validate_user_token)):
    return list_bucket_files()


@app.post("/api/v1/upload")
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(),
    user_email: str = Depends(validate_user_token)
):
    contents = await file.read()
    print(file.filename)
    result = write_file_shared_storage(contents, file.filename)
    scanner = Scanner(file.filename, user_email["email"])
    scanner.scanner_audit()
    background_tasks.add_task(scanner.scanner_init)
    return {"response": result}


@app.post("/api/v1/user_token")
async def token(user_access_token: str = Form()):
    login_handler = LoginHandler(user_access_token, engine)
    try: 
        login_handler.create_user()
    except Exception as e:
        print(f"Error: {e}")
    response = auth_user_data(user_access_token)
    if response.status_code != 200:
        return response.status_code
    return response.json()

@app.get("/api/v1/login")
async def login(code: str | None = None):
    if code:
        response = token_resolve(code)
        access_token = response.get("access_token")
        if (access_token):
            return HTMLResponse(f"""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>Success</title>
                    <style>
                        .code-box {{
                            background: #f5f5f5;
                            padding: 15px;
                            border-radius: 8px;
                            cursor: pointer;
                            margin: 20px 0;
                            font-family: monospace;
                            font-size: 18px;
                        }}
                        .code-box:hover {{
                            background: #e8e8e8;
                        }}
                    </style>
                </head>
                <body>
                    <h1>Authentication Successful!</h1>
                    <p>Click the code below to copy:</p>
                    <div class="code-box" onclick="copy(this)">
                        {access_token}
                    </div>
                    <p id="status"></p>

                    <script>
                        function copy(el) {{
                            navigator.clipboard.writeText(el.textContent.trim());
                            document.getElementById('status').textContent = '✓ Copied to clipboard!';
                        }}
                    </script>
                </body>
                </html>
                """)
        else:
            raise ValueError("No Access Token")

    else:
        return oauth_redirect()

