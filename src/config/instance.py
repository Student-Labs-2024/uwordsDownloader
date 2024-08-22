import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).parent.parent.parent

SECRET_TOKEN: str = os.environ.get("SECRET_TOKEN")
PIX_TOKEN: str = os.environ.get("PIX_TOKEN")

YOUTUBE_UPLOAD_DIR = BASE_DIR / "download" / "youtube"
IMAGE_UPLOAD_DIR = BASE_DIR / "download" / "images"

ALLOWED_ORIGINS: str = os.environ.get("ALLOWED_ORIGINS")
ALLOWED_ORIGINS_LIST = ALLOWED_ORIGINS.split(",")
PIC_QUALITY = 20  # can be from 1 to 95, the lower the number, the worse the quality
