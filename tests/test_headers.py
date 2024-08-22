import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from src.config.instance import SECRET_TOKEN
from src.utils.headers import check_secret_token


class TestHeaders:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "token, expected_result",
        [
            (f"{SECRET_TOKEN}", True),
            ("invalid_token", HTTPException),
        ],
    )
    async def test_check_secret_token(self, token, expected_result):
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)

        if isinstance(expected_result, bool):
            result = await check_secret_token(credentials)
            assert result == expected_result
        else:
            with pytest.raises(expected_result):
                await check_secret_token(credentials)
