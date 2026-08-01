from app.repositories.user_repo import UserRepo
from app.utils.validators import validate_password
from app.auth.passward import passward_hash, passward_verify
from app.models.user import User
from sqlmodel import Session


class AuthService:

    @staticmethod
    def register_user(session: Session, username, email, passward):

        validate_password(passward)

        existing_email = UserRepo.get_user_by_email(session, email)
        existing_username = UserRepo.get_user_by_name(session, username)

        if existing_email or existing_username:
            return None

        user = User(
            username=username, email=email, passward_hash=passward_hash(passward)
        )

        return UserRepo.create_user(session, user)

    @staticmethod
    def authenticate_user(session: Session, email, passward):

        user = UserRepo.get_user_by_email(session, email)

        if not user:
            return None

        verify_passward = passward_verify(passward, user.passward_hash)

        if not verify_passward:
            return None

        return user

    @staticmethod
    def update_username(old_username, new_username, session: Session):

        if UserRepo.get_user_by_name(session, new_username):
            return None  # already taken

        user = UserRepo.get_user_by_name(session, old_username)

        if not user:
            return None

        user.username = new_username

        return UserRepo.update_user(session, user)

    @staticmethod
    def update_email(old_email, new_email, session: Session):

        if UserRepo.get_user_by_email(session, new_email):
            return None  # already taken

        user = UserRepo.get_user_by_email(session, old_email)

        if not user:
            return None

        user.email = new_email

        return UserRepo.update_user(session, user)
