import logging

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from config.instance import SECRET_TOKEN


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s][%(name)s]%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger("UTILS HEADERS")


http_bearer = HTTPBearer()


async def check_secret_token(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> dict:
    token = credentials.credentials

    if token != SECRET_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail={"msg": "Permission denied"}
        )

    return True
