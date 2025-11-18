#from pydantic import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "API OCR")
VERSION = os.getenv("VERSION", "1.0.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
TESSERACT_LINUX_CMD = os.getenv("TESSERACT_LINUX_CMD")
TESSERACT_WINDOWS_CMD = os.getenv("TESSERACT_WINDOWS_CMD")

