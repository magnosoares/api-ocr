from fastapi import FastAPI
import logging
from fastapi.middleware.cors import CORSMiddleware
from src.config import APP_NAME, VERSION, CORS_ORIGINS, ENVIRONMENT, LOG_LEVEL, TESSERACT_LINUX_CMD, TESSERACT_WINDOWS_CMD

from src.api.routes.recognition import router as recognition_router
from src.api.routes.search import router as search_router
from src.api.routes.health import router as health_router
from src.api.routes.about import router as about_router

# Environment
APP_NAME = APP_NAME,
VERSION = VERSION,
ENVIRONMENT = ENVIRONMENT,
LOG_LEVEL = LOG_LEVEL,
CORS_ORIGINS = CORS_ORIGINS
tesseract_cmd = TESSERACT_LINUX_CMD
#tesseract_cmd = TESSERACT_WINDOWS_CMD

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
        },
        {
            "name": "Search",
            "description": "Methods to search text from files"
        },
        {
            "name": "About",
            "description": "Developers Team"
        }
    ]
)


# ==================
# CORS Config
# ==================
app.add_middleware(
    CORSMiddleware,
    allow_origins = CORS_ORIGINS,
    allow_credentials = True, 
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

# Search route
app.include_router(search_router)

# About route
app.include_router(about_router)
