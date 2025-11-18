# api-ocr/src/api/routes/health.py

from fastapi import APIRouter
from src.config import  APP_NAME, VERSION, ENVIRONMENT

router = APIRouter(prefix="/health", tags = ["Health"])

@router.get("/", status_code = 200)
def health():
    """Endpoint de Health check"""
    return {
        "status": "ok", 
        "message": "API funcionando",
        "app": APP_NAME,
        "version": VERSION,
        "environment": ENVIRONMENT
    }
