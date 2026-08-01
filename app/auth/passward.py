from passlib.context import CryptContext

pswd = CryptContext(schemes=["bcrypt"], deprecated="auto")


def passward_hash(passward: str):

    return pswd.hash(passward)


def passward_verify(plain_passward, hash_passward):

    return pswd.verify(plain_passward, hash_passward)
