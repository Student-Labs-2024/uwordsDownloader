import logging
import aiohttp
import aiofiles
from PIL import Image
from typing import Tuple

from src.config.instance import PIX_TOKEN, IMAGE_UPLOAD_DIR, PIC_QUALITY
from src.utils.exceptions import PixabaySearchError, PixabayDownloadError


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s][%(name)s]%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger("SERVICES PIXABAY")


async def search_image(word: str) -> str:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                url="https://pixabay.com/api/",
                params={
                    "key": PIX_TOKEN,
                    "q": "+".join(word.split()),
                    "lang": "en",
                    "per_page": 3,
                },
            ) as response:
                if response.status == 200:
                    data: dict = await response.json()
                    image: dict = data.get("hits", None)[0]

                    return image.get("largeImageURL")

                else:
                    return None

        except Exception as e:
            logger.error(f"[SEARCH] Error: {e}")
            raise PixabaySearchError(f"Failed to search for image!")


async def download_pixabay_image(
    word: str,
) -> Tuple[str, str]:
    image_url = await search_image(word=word)

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(image_url) as response:
                if response.status == 200:
                    filename = f"{word}.jpg"
                    image_path = IMAGE_UPLOAD_DIR / filename

                    async with aiofiles.open(image_path, "wb") as f:
                        content = await response.read()
                        await f.write(content)

                    image = Image.open(image_path)
                    image.save(image_path, quality=PIC_QUALITY, optimize=True)

                    return image_path, filename
                else:
                    logger.info(f"[DOWNLOAD] Error: {response.text()}")
                    raise PixabayDownloadError(f"Failed to download image!")

        except Exception as e:
            logger.info(f"[DOWNLOAD] Error: {e}")
            raise PixabayDownloadError(f"Failed to download image!")
