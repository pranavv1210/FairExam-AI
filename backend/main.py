"""
FairExam AI - Main FastAPI Application
Imagine Cup 2026 MVP
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
from routes import analysis
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="FairExam AI",
    description="AI-Powered Exam Paper Fairness & Bias Detection System",
    version="1.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://*.vercel.app",
        os.getenv("FRONTEND_URL", "*")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(analysis.router, prefix="/api", tags=["Analysis"])

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "active",
        "app": "FairExam AI",
        "version": "1.0.0",
        "description": "AI-Powered Exam Paper Fairness & Bias Detection System"
    }

@app.get("/health")
async def health_check():
    """Detailed health check with Azure service status"""
    azure_openai_configured = bool(
        os.getenv("AZURE_OPENAI_ENDPOINT") and 
        os.getenv("AZURE_OPENAI_API_KEY") and 
        os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    )
    
    return {
        "status": "healthy",
        "azure_openai_configured": azure_openai_configured,
        "message": "Azure OpenAI handles all AI features" if azure_openai_configured else "Running with fallback heuristics"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
