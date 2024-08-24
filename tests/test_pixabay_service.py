from pathlib import Path
import aiohttp
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.services.pixabay_service import download_pixabay_image, search_image
from src.utils.exceptions import PixabayDownloadError, PixabaySearchError
from src.config.instance import IMAGE_UPLOAD_DIR, PIC_QUALITY, PIX_TOKEN


class TestPixabayService:
    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "word, status_code, response_json, expected_result",
        [
            (
                "cat",
                200,
                {"hits": [{"largeImageURL": "https://example.com/cat.jpg"}]},
                "https://example.com/cat.jpg",
            ),
            (
                "dog",
                200,
                {"hits": [{"largeImageURL": "https://example.com/dog.jpg"}]},
                "https://example.com/dog.jpg",
            ),
            ("bird", 404, {}, None),
            ("error", 500, {}, None),
        ],
    )
    @patch("aiohttp.ClientSession.get")
    async def test_search_image(
        mock_get, word, status_code, response_json, expected_result
    ):
        mock_response = AsyncMock()
        mock_response.status = status_code
        mock_response.json = AsyncMock(return_value=response_json)
        mock_get.return_value.__aenter__.return_value = mock_response

        result = await search_image(word)

        mock_get.assert_called_once_with(
            url="https://pixabay.com/api/",
            params={
                "key": PIX_TOKEN,
                "q": "+".join(word.split()),
                "lang": "en",
                "per_page": 3,
            },
        )
        assert result == expected_result

    @staticmethod
    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.get")
    async def test_search_image_exception(mock_get):
        mock_get.side_effect = aiohttp.ClientError("Test exception")

        with pytest.raises(PixabaySearchError):
            await search_image("exception")

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "word, status_code, response_read, expected_result",
        [
            ("cat", 200, b"test", (Path(f"{IMAGE_UPLOAD_DIR}/cat.jpg"), "cat.jpg")),
            ("dog", 200, b"test", (Path(f"{IMAGE_UPLOAD_DIR}/dog.jpg"), "dog.jpg")),
        ],
    )
    @patch("PIL.Image.open")
    @patch("src.services.pixabay_service.search_image")
    @patch("aiohttp.ClientSession.get")
    @patch("aiofiles.open")
    async def test_download_pixabay_image(
        mock_open,
        mock_get,
        mock_search_image,
        mock_image_open,
        word,
        status_code,
        response_read,
        expected_result,
    ):
        mock_search_image.return_value = "https://example.com/image.jpg"

        mock_response = AsyncMock()
        mock_response.status = status_code
        mock_response.read = AsyncMock(return_value=response_read)
        mock_get.return_value.__aenter__.return_value = mock_response

        mock_open.return_value.__aenter__.return_value = AsyncMock()

        mock_image_open.return_value = MagicMock()

        result = await download_pixabay_image(word)
        assert result == expected_result

        mock_search_image.assert_called_once_with(word=word)
        mock_get.assert_called_once_with("https://example.com/image.jpg")

    @staticmethod
    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.get")
    @patch("src.services.pixabay_service.search_image")
    async def test_download_pixabay_image_exception(mock_search_image, mock_get):
        mock_search_image.return_value = "https://example.com/exception.jpg"
        mock_get.side_effect = aiohttp.ClientError("Test exception")

        with pytest.raises(PixabayDownloadError):
            await download_pixabay_image("exception")
