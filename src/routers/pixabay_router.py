import os
from fastapi.responses import FileResponse
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status

from src.utils.headers import check_secret_token

from src.services.pixabay_service import download_pixabay_image


pixabay_router_v1 = APIRouter(prefix="/api/v1/pixabay", tags=["Pixabay"])


@pixabay_router_v1.get("/download")
async def download_image(
    word: str, background_tasks: BackgroundTasks, token=Depends(check_secret_token)
) -> str:

    file_path, filename = await download_pixabay_image(word=word)

    if not file_path:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"msg": "Something went wrong. Try again"},
        )

    background_tasks.add_task(os.remove, file_path)

    return FileResponse(path=file_path, media_type="image/jpeg", filename=filename)
