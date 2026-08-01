from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.jwt_handler import decode_access_token

security = HTTPBearer()


def get_user(credential: HTTPAuthorizationCredentials = Depends(security)):

    token = credential.credentials
    payload = decode_access_token(token)

    username = payload.get("sub")

    if not username:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Invalid"
        )

    return username
