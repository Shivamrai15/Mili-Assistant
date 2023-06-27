import os
from cryptography.fernet import Fernet

application_directory = os.getcwd()


# ------------------------------------------------------------------------------------------------------------
class Encryption:
    def __init__(self, text) -> None:
        self.text = text

    def load_key(self):
        return open(application_directory+"\\Data\\Files\\secret.key", "rb").read()

    def decrypt_text(self) -> str:
        key = self.load_key()
        f = Fernet(key)
        decrypted_text = f.decrypt(self.text)
        return decrypted_text.decode()

    def encrypt_text(self) -> bytes:
        key = self.load_key()
        encoded_text = self.text.encode(encoding="utf-8")
        f = Fernet(key)
        encrypted_text = f.encrypt(encoded_text)
        return encrypted_text
# ------------------------------------------------------------------------------------------------------------