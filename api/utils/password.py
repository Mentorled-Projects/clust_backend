from passlib.context import CryptContext

pwd= CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_passsword(password:str) -> str:
    return pwd.hash(password)

def verify_password(plain_password:str, hashed_password:str) -> bool:
    return pwd.verify(plain_password, hashed_password)