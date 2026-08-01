from datetime import datetime, timedelta, UTC
from jose import jwt, JWTError
from app.core.config import get_setting

setting = get_setting()

secret_key = setting.SECRET_KEY
algorithm = "HS256"
expire = 30


def encode_access_token(user: dict):

    to_encode = user.copy()
    exp = datetime.now(UTC) + timedelta(minutes=expire)
    to_encode.update({"exp": exp})

    return jwt.encode(to_encode, secret_key, algorithm=algorithm)


def decode_access_token(token: str):

    try:
        return jwt.decode(token, secret_key, algorithms=[algorithm])
    except JWTError:
        return {"error": "The token is unable to decode due to some error"}
