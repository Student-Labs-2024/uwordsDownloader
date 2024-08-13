import logging
import aiohttp
import aiofiles
from typing import Tuple, Union

from src.config.instance import PIX_TOKEN, IMAGE_UPLOAD_DIR


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s][%(name)s]%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger("SERVICES IMAGE")


async def search_image(word: str) -> Union[str, None]:
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
            logger.info(f"[SEARCH] Error: {e}")
            return None


async def download_pixabay_image(
    word: str,
) -> Union[Tuple[str, str], Tuple[None, None]]:
    image_url = await search_image(word=word)

    if not image_url:
        return None, None

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(image_url) as response:
                if response.status == 200:
                    filename = f"{word}.jpg"
                    image_path = IMAGE_UPLOAD_DIR / filename

                    async with aiofiles.open(image_path, "wb") as f:
                        content = await response.read()
                        await f.write(content)
                    return image_path, filename
                else:
                    logger.info(f"[DOWNLOAD] Error: {response.text()}")
                    return None, None

        except Exception as e:
            logger.info(f"[DOWNLOAD] Error: {e}")
            return None, None
