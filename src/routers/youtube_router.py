import logging
import os
from fastapi.responses import FileResponse
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status

from src.utils.headers import check_secret_token
from utils.exceptions import YouTubeDownloadError

from src.services.youtube_service import (
    download_youtube_audio,
    download_youtube_subtitles,
)


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s][%(name)s]%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger("ROUTER YOUTUBE")


youtube_router_v1 = APIRouter(prefix="/api/v1/youtube", tags=["YouTube"])


@youtube_router_v1.get("/download")
async def download_youtube(
    link: str, background_tasks: BackgroundTasks, token=Depends(check_secret_token)
) -> str:
    try:

        file_path, video_title = await download_youtube_audio(link=link)

        background_tasks.add_task(os.remove, file_path)

        return FileResponse(
            path=file_path, media_type="audio/mpeg", filename=f"{video_title}.mp3"
        )

    except YouTubeDownloadError as e:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail={"msg": str(e)},
        )

    except Exception as e:
        logger.info(f"[DOWNLOAD] Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail={"msg": "Failed to download audio!"},
        )


@youtube_router_v1.get("/subtitles")
async def subtitles_youtube(
    link: str, background_tasks: BackgroundTasks, token=Depends(check_secret_token)
) -> str:
    try:

        file_path = await download_youtube_subtitles(link=link)

        background_tasks.add_task(os.remove, file_path)

        return FileResponse(path=file_path, media_type="text/plain")

    except YouTubeDownloadError as e:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail={"msg": str(e)},
        )

    except Exception as e:
        logger.info(f"[SUBTITLES] Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail={"msg": "Failed to download subtitles!"},
        )
