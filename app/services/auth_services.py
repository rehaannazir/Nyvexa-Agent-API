from app.repositories.user_repo import UserRepo
from app.utils.validators import validate_password
from app.auth.passward import passward_hash, passward_verify
from app.models.user import User
from app.core.logging import logger
from sqlmodel import Session


class AuthService:

    @staticmethod
    def register_user(session: Session, username, email, passward):

        validate_password(passward)

        existing_email = UserRepo.get_user_by_email(session, email)
        existing_username = UserRepo.get_user_by_name(session, username)

        if existing_email or existing_username:
            logger.warning(
                "Registration failed: username '%s' or email '%s' already exists.",
                username,
                email,
            )
            return None

        user = User(
            username=username, email=email, passward_hash=passward_hash(passward)
        )

        created = UserRepo.create_user(session, user)
        logger.info("User '%s' registered successfully.", username)

        return created

    @staticmethod
    def authenticate_user(session: Session, email, passward):

        user = UserRepo.get_user_by_email(session, email)

        if not user:
            logger.warning("Login failed: no user with email '%s'.", email)
            return None

        verify_passward = passward_verify(passward, user.passward_hash)

        if not verify_passward:
            logger.warning("Login failed: wrong password for user '%s'.", user.username)
            return None

        logger.info("User '%s' logged in successfully.", user.username)

        return user

    @staticmethod
    def update_username(old_username, new_username, session: Session):

        if UserRepo.get_user_by_name(session, new_username):
            logger.warning("Username update failed: '%s' already taken.", new_username)
            return None  # already taken

        user = UserRepo.get_user_by_name(session, old_username)

        if not user:
            logger.warning("Username update failed: '%s' not found.", old_username)
            return None

        user.username = new_username

        updated = UserRepo.update_user(session, user)
        logger.info("Username updated: '%s' -> '%s'.", old_username, new_username)

        return updated

    @staticmethod
    def update_email(old_email, new_email, session: Session):

        if UserRepo.get_user_by_email(session, new_email):
            logger.warning("Email update failed: '%s' already taken.", new_email)
            return None  # already taken

        user = UserRepo.get_user_by_email(session, old_email)

        if not user:
            logger.warning("Email update failed: '%s' not found.", old_email)
            return None

        user.email = new_email

        updated = UserRepo.update_user(session, user)
        logger.info("Email updated: '%s' -> '%s'.", old_email, new_email)

        return updated
