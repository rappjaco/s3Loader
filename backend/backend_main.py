from fastapi import FastAPI, File, UploadFile, BackgroundTasks, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from backend_upload import write_file_shared_storage, list_bucket_files
from backend_scanner import Scanner
from pydantic import BaseModel
from backend_auth import oauth_redirect, token_resolve, auth_user_data

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
    return {"response": result}


@app.post("/api/v1/user_token")
async def token(user_access_token: str = Form()):
    response = auth_user_data(user_access_token)
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
