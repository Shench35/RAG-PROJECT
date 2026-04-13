from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.app.main import main_route
from src.auth.routes import auth_router
from fastapi import Request
from fastapi.responses import JSONResponse, Response
from src.app.admin.admin import admin_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.app.services.config import Config
import os


app = FastAPI(
    title="RAG API",
    description="A simple Retrieval-Augmented Generation (RAG) API using FastAPI, ChromaDB, and Ollama.",
    version="1.0.0"
)

# Bulletproof Health Check Middleware for Render
@app.middleware("http")
async def render_health_check_middleware(request: Request, call_next):
    if request.method == "HEAD":
        return Response(status_code=200)
    return await call_next(request)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Health check for Render (Handles GET)
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# 2. Serve specific frontend pages at the root level BEFORE static/catch-all
@app.get("/admin.html")
async def admin_page():
    return FileResponse("src/frontend/admin.html")

@app.get("/login.html")
async def login_page():
    return FileResponse("src/frontend/login.html")

# 3. Handle Landing Page (GET)
@app.get("/")
async def landing():
    return FileResponse("src/frontend/index.html")

# 4. Serve static files
app.mount("/static", StaticFiles(directory="src/frontend"), name="static")

# 5. Catch-all for other HTML pages
@app.get("/{page_name}.html")
async def get_page(page_name: str):
    file_path = f"src/frontend/{page_name}.html"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="Page not found")

app.include_router(main_route) 
app.include_router(auth_router) 
app.include_router(admin_router)
