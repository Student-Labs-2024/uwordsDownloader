import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).parent.parent.parent

SECRET_TOKEN: str = os.environ.get("SECRET_TOKEN")
PIX_TOKEN_1: str = os.environ.get("PIX_TOKEN_1")
PIX_TOKEN_2: str = os.environ.get("PIX_TOKEN_2")
PIX_TOKEN_3: str = os.environ.get("PIX_TOKEN_3")
PIX_TOKEN_4: str = os.environ.get("PIX_TOKEN_4")
PIX_TOKEN_5: str = os.environ.get("PIX_TOKEN_5")
PIX_TOKEN_6: str = os.environ.get("PIX_TOKEN_6")
REQUEST_LIMIT_PER_MINUTE: int = 100
API_KEYS = [
    PIX_TOKEN_1,
    PIX_TOKEN_2,
    PIX_TOKEN_3,
    PIX_TOKEN_4,
    PIX_TOKEN_5,
    PIX_TOKEN_6,
]

YOUTUBE_UPLOAD_DIR = BASE_DIR / "download" / "youtube"
IMAGE_UPLOAD_DIR = BASE_DIR / "download" / "images"

ALLOWED_ORIGINS: str = os.environ.get("ALLOWED_ORIGINS")
ALLOWED_ORIGINS_LIST = ALLOWED_ORIGINS.split(",")
PIC_QUALITY = 20  # can be from 1 to 95, the lower the number, the worse the quality
