import logging
import aiohttp
import aiofiles
import traceback
from time import time
from PIL import Image
from typing import Dict, Tuple
from collections import defaultdict

from src.utils.exceptions import (
    PixabayAPIKeyError,
    PixabaySearchError,
    PixabayDownloadError,
)
from src.config.instance import (
    API_KEYS,
    IMAGE_UPLOAD_DIR,
    PIC_QUALITY,
    REQUEST_LIMIT_PER_MINUTE,
)


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s][%(name)s]%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger("SERVICES PIXABAY")

KEY_USAGE: Dict[str, Tuple[int, float]] = defaultdict(lambda: (0, time()))


async def get_available_key() -> str:
    current_time = time()

    for key in API_KEYS:
        usage_count, last_reset_time = KEY_USAGE.get(key, (0, current_time))

        if current_time - last_reset_time > 60:
            KEY_USAGE[key] = (0, current_time)
            return key

        if usage_count < REQUEST_LIMIT_PER_MINUTE:
            KEY_USAGE[key] = (usage_count + 1, last_reset_time)
            return key

    raise PixabayAPIKeyError(
        "All API keys have reached their request limits. Please wait."
    )


async def search_image(word: str) -> str:
    try:
        key = await get_available_key()

    except PixabayAPIKeyError as e:
        logger.error(f"[SEARCH] Error: {e}\n{traceback.format_exc()}")
        raise PixabaySearchError("Failed to find active API key!")

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                url="https://pixabay.com/api/",
                params={
                    "key": key,
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
                    logger.error(f"[SEARCH] Error: {response.text()}")
                    return None

        except Exception as e:
            logger.error(f"[SEARCH] Error: {e}\n{traceback.format_exc()}")
            raise PixabaySearchError(f"Failed to search for image!")


async def download_pixabay_image(
    word: str,
) -> Tuple[str, str]:
    image_url = await search_image(word=word)

    if not image_url:
        raise PixabayDownloadError(f"No image URL returned for word: {word}")

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
            logger.info(f"[DOWNLOAD] Error: {e}\n{traceback.format_exc()}")
            raise PixabayDownloadError(f"Failed to download image!")
