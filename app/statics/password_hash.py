from passlib.context import CryptContext

crypt_context = CryptContext(schemes=['bcrypt'])

class PasswordProtector:
    @staticmethod
    def hashPassword(plain_text):
        return crypt_context.hash(secret=plain_text)
    
    @staticmethod
    def verifyPassword(plain_text,hashed_password):
        return crypt_context.verify(secret=plain_text,hash=hashed_password)