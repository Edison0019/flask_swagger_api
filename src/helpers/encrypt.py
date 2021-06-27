from hashlib import pbkdf2_hmac
from uuid import uuid4

class EncryptPassword:
    def __init__(self,password) -> None:
        self.password = password
    
    def get_salt(self):
        salt = uuid4()
        return salt.bytes

    def encript(self,salt):
        key = pbkdf2_hmac(
            'sha256',
            self.password.encode('utf-8'),
            salt,
            100000
        )
        return key
