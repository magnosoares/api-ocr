from fastapi import FastAPI, HTTPException, File, UploadFile
from src.models.schemas import ImageUploadForOCR
import logging
import pytesseract
from PIL import Image
import io
import re
from dotenv import load_dotenv

from src.api.routes.recognition import router as recognition_router
from src.api.routes.health import router as health_router

# Loading environment 
load_dotenv()

# Environment
APP_NAME = os.getenv("APP_NAME", "API OCR")
VERSION = os.getenv("VERSION", "1.0.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


# Caminho do executável
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title = "API - Automação OCR",
    version = "0.1.0",
    description = "API for OCR text extraction from images",
    openapi_tags = [
        {
            "name": "Health",
            "description": "Returns the API health status"
        },
        {
            "name": "Recognition",
            "description": "Methods to extrat text from images"
        }
    ]
)


# ==================
# CORS Config
# ==================
app.add_middleware(
    CORSMiddleware,
    allow_origins = CORS_ORIGINS,
    allow_cretentials = True, 
    allow_methods = ["*"], 
    allow_headers = ["*"]
)


# ======================================
# ROUTES
# ======================================

# health-check route
app.include_router(recognition_router)

# Recognition route
app.include_router(health_router)
