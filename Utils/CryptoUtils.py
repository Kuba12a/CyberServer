import zlib

from cryptography.fernet import Fernet


def compress(message: bytes):
    return zlib.compress(message, zlib.Z_BEST_COMPRESSION)


def decompress(message: bytes):
    return zlib.decompress(message)


def encode_ascii(text: str):
    return text.encode('ascii')


def decode_ascii(message: bytes):
    return message.decode('ascii')


def encrypt(message: bytes, encryption_key: str):
    f = Fernet(encryption_key)

    return f.encrypt(message)


def decrypt(message: bytes, encryption_key: str):
    f = Fernet(encryption_key)

    return f.decrypt(message)
