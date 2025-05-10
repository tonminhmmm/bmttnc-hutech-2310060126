# cipher/rsa/rsa_cipher.py
from Crypto.PublicKey import RSA
from Crypto.Cipher    import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash      import SHA256

class RSACipher:
    def generate_keys(self, key_size=2048):
        key = RSA.generate(key_size)
        priv = key.export_key()
        pub  = key.publickey().export_key()
        with open("private.pem","wb") as f: f.write(priv)
        with open("public.pem","wb")  as f: f.write(pub)

    def load_keys(self):
        with open("private.pem","rb") as f: priv = RSA.import_key(f.read())
        with open("public.pem", "rb") as f: pub  = RSA.import_key(f.read())
        return priv, pub

    def encrypt(self, message: str, key) -> bytes:
        cipher = PKCS1_OAEP.new(key)
        return cipher.encrypt(message.encode())

    def decrypt(self, ciphertext: bytes, key) -> str:
        cipher = PKCS1_OAEP.new(key)
        return cipher.decrypt(ciphertext).decode()

    def sign(self, message: str, key) -> bytes:
        h = SHA256.new(message.encode())
        return pkcs1_15.new(key).sign(h)

    def verify(self, message: str, signature: bytes, key) -> bool:
        h = SHA256.new(message.encode())
        try:
            pkcs1_15.new(key).verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False
