from fastapi import HTTPException, Request, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from app.auth.jwt_handler import decode_access_token
from app.core.database import get_session
from app.models.user import User
from app.repositories.user_repo import UserRepo
from app.core.logging import logger

security = HTTPBearer()


def get_user(
    request: Request,
    credential: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session),
) -> User:

    token = credential.credentials
    payload = decode_access_token(token)

    username = payload.get("sub")

    if not username:

        logger.warning("Rejected request: invalid or undecodable token.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Invalid"
        )

    user = UserRepo.get_user_by_name(session, username)

    if not user:

        logger.warning("Rejected request: token valid but user '%s' not found.", username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    request.state.user = user

    return user
