from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.app.main import main_route
from src.auth.routes import auth_router



app = FastAPI(
    title="RAG API",
    description="A simple Retrieval-Augmented Generation (RAG) API using FastAPI, ChromaDB, and Ollama.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",  # ← this is the one hitting your backend
    ],  # VS Code Live Server default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_route) 
app.include_router(auth_router) 