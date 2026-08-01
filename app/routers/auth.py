from app.schemas.user_schema import (
    TokenResponse,
    UserCreate,
    UserLogin,
    UserNameUpdate,
    UserEmailUpdate,
)
from app.auth.jwt_handler import encode_access_token
from app.services.auth_services import AuthService
from app.core.database import get_session
from fastapi import HTTPException, status, Depends
from fastapi.routing import APIRouter

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, session=Depends(get_session)):

    user = AuthService.register_user(session, user.name, user.email, user.passward)

    if not user:
        raise HTTPException(
            detail="Error occured! user may already exist.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return {"message": "User is registered successfully."}


@router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenResponse)
def login_user(user: UserLogin, session=Depends(get_session)):

    user_b = AuthService.authenticate_user(session, user.email, user.passward)

    if not user_b:
        raise HTTPException(
            detail="Error occured! user may not exist or passward incorrect.",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    token = encode_access_token({"sub": user_b.username})

    return {"access_token": token, "token_type": "bearer"}


@router.post("/update-username", status_code=status.HTTP_200_OK)
def update_username(user: UserNameUpdate, session=Depends(get_session)):

    updated = AuthService.update_username(user.old_username, user.new_username, session)

    if not updated:
        raise HTTPException(
            detail="ERROR: The username already exist or user not found",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return {"message": f"Username is updated successfully to {updated.username}"}


@router.post("/update-email", status_code=status.HTTP_200_OK)
def update_email(user: UserEmailUpdate, session=Depends(get_session)):

    updated = AuthService.update_email(user.old_email, user.new_email, session)

    if not updated:
        raise HTTPException(
            detail="ERROR: The email already exist or user not found",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return {"message": f"Email is updated successfully to {updated.email}"}
