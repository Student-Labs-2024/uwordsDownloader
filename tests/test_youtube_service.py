import pytest
from unittest.mock import patch, MagicMock
from src.services.youtube_service import (
    download_youtube_audio,
    download_youtube_subtitles,
)
from src.utils.exceptions import YouTubeDownloadError


class TestYoutubeService:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "link, info_dict, expected_result",
        [
            (
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                {
                    "title": "Rick Astley - Never Gonna Give You Up (Official Music Video)",
                    "ext": "webm",
                },
                (
                    "/path/to/Rick_Astley_-_Never_Gonna_Give_You_Up_(Official_Music_Video).mp3",
                    "Rick_Astley_-_Never_Gonna_Give_You_Up_(Official_Music_Video)",
                ),
            ),
            (
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                {
                    "title": "Rick Astley - Never Gonna Give You Up (Official Music Video)",
                    "ext": "m4a",
                },
                (
                    "/path/to/Rick_Astley_-_Never_Gonna_Give_You_Up_(Official_Music_Video).mp3",
                    "Rick_Astley_-_Never_Gonna_Give_You_Up_(Official_Music_Video)",
                ),
            ),
        ],
    )
    @patch("yt_dlp.YoutubeDL")
    async def test_download_youtube_audio(
        self, mock_yt_dlp, link, info_dict, expected_result
    ):
        mock_ydl = MagicMock()
        mock_ydl.extract_info.return_value = info_dict
        mock_ydl.prepare_filename.return_value = f"/path/to/{info_dict.get('title', '').replace(' ', '_')}.{info_dict.get('ext', '')}"
        mock_yt_dlp.return_value.__enter__.return_value = mock_ydl

        result = await download_youtube_audio(link)
        assert result == expected_result

    @staticmethod
    @pytest.mark.asyncio
    @patch("yt_dlp.YoutubeDL")
    async def test_download_youtube_audio_exception(mock_yt_dlp):
        mock_ydl_instance = MagicMock()
        mock_yt_dlp.return_value.__enter__.return_value = mock_ydl_instance

        mock_ydl_instance.extract_info.side_effect = Exception("Test exception")

        with pytest.raises(YouTubeDownloadError):
            await download_youtube_audio("https://example.com/video_exception")

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "link, info_dict, lang1, lang2, expected_result",
        [
            (
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                {
                    "title": "Rick Astley - Never Gonna Give You Up (Official Music Video)",
                    "subtitles": {"en": "subtitles_en.vtt", "ru": "subtitles_ru.vtt"},
                },
                "en",
                "ru",
                "/path/to/Rick_Astley_-_Never_Gonna_Give_You_Up_(Official_Music_Video)",
            ),
            (
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                {
                    "title": "Rick Astley - Never Gonna Give You Up (Official Music Video)",
                    "subtitles": {"ru": "subtitles_ru.vtt"},
                },
                "en",
                "ru",
                "/path/to/Rick_Astley_-_Never_Gonna_Give_You_Up_(Official_Music_Video)",
            ),
        ],
    )
    @patch("yt_dlp.YoutubeDL")
    async def test_download_youtube_subtitles(
        self, mock_yt_dlp, link, info_dict, lang1, lang2, expected_result
    ):
        mock_ydl = MagicMock()
        mock_ydl.extract_info.return_value = info_dict
        mock_ydl.prepare_filename.return_value = (
            f"/path/to/{info_dict.get('title', '').replace(' ', '_')}"
        )
        mock_yt_dlp.return_value.__enter__.return_value = mock_ydl

        result = await download_youtube_subtitles(link, lang1, lang2)
        assert result == expected_result

    @staticmethod
    @pytest.mark.asyncio
    @patch("yt_dlp.YoutubeDL")
    async def test_download_youtube_subtitles_no_subtitles(mock_yt_dlp):
        mock_ydl_instance = MagicMock()
        mock_yt_dlp.return_value.__enter__.return_value = mock_ydl_instance

        mock_info_dict = {
            "title": "video1 title",
            "ext": "vtt",
        }
        mock_ydl_instance.extract_info.return_value = mock_info_dict

        with pytest.raises(YouTubeDownloadError):
            await download_youtube_subtitles(
                "https://example.com/video_no_subtitles", "en", "ru"
            )

    @staticmethod
    @pytest.mark.asyncio
    @patch("yt_dlp.YoutubeDL")
    async def test_download_youtube_subtitles_exception(mock_yt_dlp):
        mock_ydl_instance = MagicMock()
        mock_yt_dlp.return_value.__enter__.return_value = mock_ydl_instance

        mock_ydl_instance.extract_info.side_effect = Exception("Test exception")

        with pytest.raises(YouTubeDownloadError):
            await download_youtube_subtitles(
                "https://example.com/video_exception", "en", "ru"
            )
