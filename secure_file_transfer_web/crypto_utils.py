# Tiện ích mã hóa, giải mã, ký số, kiểm tra hash cho hệ thống (giữ nguyên như cũ)
from Crypto.Cipher import DES, PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
import base64

def generate_rsa_keypair(bits=1024):
    key = RSA.generate(bits)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def load_rsa_private_key(pem_bytes):
    return RSA.import_key(pem_bytes)

def load_rsa_public_key(pem_bytes):
    return RSA.import_key(pem_bytes)

def rsa_encrypt(public_key, data: bytes) -> bytes:
    cipher = PKCS1_v1_5.new(public_key)
    return cipher.encrypt(data)

def rsa_decrypt(private_key, enc_data: bytes) -> bytes:
    cipher = PKCS1_v1_5.new(private_key)
    return cipher.decrypt(enc_data, None)

def rsa_sign(private_key, data: bytes) -> bytes:
    h = SHA512.new(data)
    signature = pkcs1_15.new(private_key).sign(h)
    return signature

def rsa_verify(public_key, data: bytes, signature: bytes) -> bool:
    h = SHA512.new(data)
    try:
        pkcs1_15.new(public_key).verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False

def generate_des_key() -> bytes:
    return get_random_bytes(8)

def generate_iv() -> bytes:
    return get_random_bytes(8)

def des_encrypt(key: bytes, iv: bytes, data: bytes) -> bytes:
    cipher = DES.new(key, DES.MODE_CBC, iv)
    pad_len = 8 - len(data) % 8
    data += bytes([pad_len]) * pad_len
    return cipher.encrypt(data)

def des_decrypt(key: bytes, iv: bytes, enc_data: bytes) -> bytes:
    cipher = DES.new(key, DES.MODE_CBC, iv)
    data = cipher.decrypt(enc_data)
    pad_len = data[-1]
    return data[:-pad_len]

def sha512_hash(data: bytes) -> str:
    h = SHA512.new(data)
    return h.hexdigest()

def b64encode(data: bytes) -> str:
    return base64.b64encode(data).decode()

def b64decode(data: str) -> bytes:
    return base64.b64decode(data)

if __name__ == "__main__":
    # Tạo khóa cho sender
    priv, pub = generate_rsa_keypair()
    with open("sender_private.pem", "wb") as f:
        f.write(priv)
    with open("sender_public.pem", "wb") as f:
        f.write(pub)
    # Tạo khóa cho receiver
    priv, pub = generate_rsa_keypair()
    with open("receiver_private.pem", "wb") as f:
        f.write(priv)
    with open("receiver_public.pem", "wb") as f:
        f.write(pub)
    print("Đã tạo đủ 4 file key .pem")
