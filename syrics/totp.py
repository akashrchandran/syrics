import requests
import hashlib
import time
from pyotp import TOTP

class SpotifyTotp:

    def base32_from_bytes(self, data, secret_sauce):
        t, n, r = 0, 0, ""
        for byte in data:
            n = (n << 8) | byte
            t += 8
            while t >= 5:
                r += secret_sauce[(n >> (t - 5)) & 31]
                t -= 5
        if t > 0:
            r += secret_sauce[(n << (5 - t)) & 31]
        return r

    def clean_buffer(self, hex_str):
        hex_str = hex_str.replace(" ", "")
        return bytes.fromhex(hex_str)

    def generate_totp(self):
        secret_sauce = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
        secret_cipher_bytes = [12, 56, 76, 33, 88, 44, 88, 33, 78, 78, 11, 66, 22, 22, 55, 69, 54]
        secret_cipher_bytes = [(e ^ (t % 33 + 9)) for t, e in enumerate(secret_cipher_bytes)]
        
        secret_bytes = bytes.fromhex(''.join(format(b, '02x') for b in bytes(''.join(map(str, secret_cipher_bytes)), 'utf-8')))
        
        secret = self.base32_from_bytes(secret_bytes, secret_sauce)
        
        totp = TOTP(secret, digits=6, digest=hashlib.sha1, interval=30)
        return totp.now()

