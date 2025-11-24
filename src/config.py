# from pydantic import BaseSettings
import logging
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "API OCR")
VERSION = os.getenv("VERSION", "1.0.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
TESSERACT_LINUX_CMD = os.getenv("TESSERACT_LINUX_CMD")
TESSERACT_WINDOWS_CMD = os.getenv("TESSERACT_WINDOWS_CMD")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


def setup_logging():
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        handlers=[logging.FileHandler(LOG_DIR / "app.log"), logging.StreamHandler()],
    )
