import os
import uuid
import yt_dlp
import logging
from typing import Tuple, Union

from src.config.instance import YOUTUBE_UPLOAD_DIR
from src.utils.exceptions import YouTubeDownloadError


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s][%(name)s]%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger("SERVICES YOUTUBE")


async def download_youtube_audio(
    link: str,
) -> Tuple[str, str]:
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
        raise YouTubeDownloadError(f"Failed to download audio!")


async def download_youtube_subtitles(
    link: str, lang1: str = "en", lang2: str = "ru"
) -> str:
    try:
        ydl_opts = {
            "writesubtitles": True,
            "subtitlesformat": "srt",
            "subtitleslangs": [lang1, lang2],
            "skip_download": True,
            "outtmpl": os.path.join(YOUTUBE_UPLOAD_DIR, "%(title)s.%(ext)s"),
            "subtitlesprefix": "",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)

            if not "subtitles" in info_dict:
                raise YouTubeDownloadError(f"Failed to download subtitles!")

            if "subtitles" in info_dict and lang1 in info_dict["subtitles"]:
                lang = lang1

            if "subtitles" in info_dict and lang2 in info_dict["subtitles"]:
                lang = lang2

            subtitle_filename = (
                ydl.prepare_filename(info_dict)
                .replace(".webm", f".{lang}.vtt")
                .replace(".m4a", f".{lang}.vtt")
            )
            ydl.download([link])
            return subtitle_filename

    except Exception as e:
        logger.info(f"[SUBTITLES] Error: {e}")
        raise YouTubeDownloadError(f"Failed to download subtitles!")
