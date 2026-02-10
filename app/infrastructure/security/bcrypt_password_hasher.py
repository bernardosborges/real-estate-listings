from passlib.context import CryptContext

class BcryptPasswordHasher():

    def __init__(self):
        self._context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    
    def hash(self, password: str) -> str:
        return self._context.hash(password)


    def verify(self, raw_password: str, hashed_password: str) -> bool:
        return self._context.verify(raw_password, hashed_password)