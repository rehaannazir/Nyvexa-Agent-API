from passlib.context import CryptContext

pswd = CryptContext(schemes=["bcrypt"], deprecated="auto")


def passward_hash(passward: str):

    return pswd.hash(passward)


def passward_verify(hash_passward, plain_passward):

    return pswd.verify(hash_passward, plain_passward)
