import os
import yt_dlp
import logging
from typing import Tuple, Union

from src.config.instance import YOUTUBE_UPLOAD_DIR


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s][%(name)s]%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger("SERVICES YOUTUBE")


async def download_youtube_audio(
    link: str,
) -> Union[Tuple[str, str], Tuple[None, None]]:
    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(YOUTUBE_UPLOAD_DIR, "%(title)s.%(ext)s"),
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            file_path = ydl.prepare_filename(info_dict)
            file_path = file_path.replace(".webm", ".mp3").replace(".m4a", ".mp3")

            title: str = info_dict.get("title", None)
            video_title = "_".join(title.split())

            return file_path, video_title

    except Exception as e:
        logger.info(f"[DOWNLOAD] Error: {e}")
        return None, None
