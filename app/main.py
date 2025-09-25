"""
Main FastAPI application entry point.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import create_tables
from app.api.messages import router as messages_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_tables()
    yield
    # Shutdown
    pass

app = FastAPI(
    title="Chat Message Processing API",
    description="A simple API for processing chat messages",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(messages_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Chat Message Processing API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)