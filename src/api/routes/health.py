# api-ocr/src/api/routes/health.py

from fastapi import APIRouter

router = APIRouter(prefix="/health", tags = ["Health"])

@router.get("/", status_code = 200)
def api_ocr():
    """Endpoint de Health check"""
    return {"status": "ok", "message": "API funcionando"}
