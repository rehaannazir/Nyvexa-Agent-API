from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from app.auth.jwt_handler import decode_access_token
from app.core.database import get_session
from app.models.user import User
from app.repositories.user_repo import UserRepo

security = HTTPBearer()


def get_user(
    credential: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session),
) -> User:

    token = credential.credentials
    payload = decode_access_token(token)

    username = payload.get("sub")

    if not username:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Invalid"
        )

    user = UserRepo.get_user_by_name(session, username)

    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    return user
