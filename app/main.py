"""
FastAPI entry point for Avatar AI Agent
"""

from fastapi import FastAPI
from app.api.routes import router
from app.core.config import settings

app = FastAPI(
    title="Avatar AI Agent",
    description="An AI agent that can execute various actions",
    version="1.0.0"
)

# Include API routes
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Avatar AI Agent is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
