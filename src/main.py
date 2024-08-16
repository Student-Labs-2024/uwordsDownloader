from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.fastapi_docs_config import TAGS_METADATA
from src.config.instance import ALLOWED_ORIGINS_LIST

from src.routers.pixabay_router import pixabay_router_v1
from src.routers.youtube_router import youtube_router_v1


app = FastAPI(
    title="UWords Downloader FastAPI",
    description="API for downloading content from foreign services",
    openapi_tags=TAGS_METADATA,
)

origins = [
    "http://localhost:5173",
    "https://localhost:5173",
    "http://localhost",
    "http://localhost:8001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS_LIST,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pixabay_router_v1)
app.include_router(youtube_router_v1)
