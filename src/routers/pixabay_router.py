import os
import logging

from fastapi.responses import FileResponse
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status

from src.utils.headers import check_secret_token
from src.utils.exceptions import PixabaySearchError, PixabayDownloadError

from src.services.pixabay_service import download_pixabay_image


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s][%(name)s]%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger("ROUTER PIXABAY")


pixabay_router_v1 = APIRouter(prefix="/api/v1/pixabay", tags=["Pixabay"])


@pixabay_router_v1.get("/download")
async def download_image(
    word: str, background_tasks: BackgroundTasks, token=Depends(check_secret_token)
) -> str:

    try:
        file_path, filename = await download_pixabay_image(word=word)

        background_tasks.add_task(os.remove, file_path)

        return FileResponse(path=file_path, media_type="image/jpeg", filename=filename)

    except PixabaySearchError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"msg": str(e)},
        )

    except PixabayDownloadError as e:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail={"msg": str(e)},
        )

    except Exception as e:
        logger.error(f"[DOWNLOAD] Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail={"msg": "Failed to download image!"},
        )
