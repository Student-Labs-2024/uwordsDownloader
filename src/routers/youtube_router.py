from fastapi.responses import FileResponse
from fastapi import APIRouter, Depends, HTTPException, status

from src.utils.headers import check_secret_token

from src.services.youtube_service import download_youtube_audio


youtube_router_v1 = APIRouter(prefix="/api/v1/youtube", tags=["YouTube"])


@youtube_router_v1.post("/download")
async def download_youtube(link: str, token=Depends(check_secret_token)) -> str:

    file_path, video_title = await download_youtube_audio(link=link)

    if not file_path:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"msg": "Something went wrong. Try again"},
        )

    return FileResponse(
        path=file_path, media_type="audio/mpeg", filename=f"{video_title}.mp3"
    )
