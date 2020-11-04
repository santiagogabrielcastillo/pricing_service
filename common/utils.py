import re
from passlib.hash import pbkdf2_sha512 # encriptacion con algoritmo pbkdf2


class Utils:
    @staticmethod
    def email_is_valid(email: str) -> bool:
        pattern = re.compile(r'^[\w-]+@([\w-]+\.)+[\w]+$')
        return True if pattern.match(email) else False

    @staticmethod
    def hash_password(password: str) -> str:
        return pbkdf2_sha512.hash(password)  # devuelve password encriptado

    @staticmethod
    def check_hash_password(password:str, hashed_password:str) -> bool:
        return pbkdf2_sha512.verify(password, hashed_password)  # encripta pass y compara con pass encriptado de la db
