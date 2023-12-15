from passlib.hash import bcrypt
from jose import jwt


def hash_passord(unhashed: str):
    return bcrypt.hash(unhashed)


def verify_hash(unhashed: str, hash: str):
    return bcrypt.verify(unhashed, hash)
