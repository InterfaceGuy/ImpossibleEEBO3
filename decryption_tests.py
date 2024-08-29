import random
import string
from itertools import cycle
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def vigenere_decrypt(ciphertext, key):
    decrypted = []
    key_cycle = cycle(key.upper())
    for char in ciphertext:
        if char.isalpha():
            shift = ord(next(key_cycle)) - ord('A')
            if char.isupper():
                decrypted.append(chr((ord(char) - shift - 65) % 26 + 65))
            else:
                decrypted.append(chr((ord(char) - shift - 97) % 26 + 97))
        else:
            decrypted.append(char)
    return ''.join(decrypted)

def prng_decrypt(ciphertext, seed):
    random.seed(seed)
    decrypted = []
    for char in ciphertext:
        if char.isalpha():
            shift = random.randint(0, 25)
            if char.isupper():
                decrypted.append(chr((ord(char) - shift - 65) % 26 + 65))
            else:
                decrypted.append(chr((ord(char) - shift - 97) % 26 + 97))
        else:
            decrypted.append(char)
    return ''.join(decrypted)

def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def aes_decrypt(ciphertext, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()

def substitution_decrypt(ciphertext, key):
    decryption_table = str.maketrans(key, string.ascii_uppercase)
    return ciphertext.translate(decryption_table)

def transposition_decrypt(ciphertext, key):
    key_order = sorted(range(len(key)), key=lambda k: key[k])
    plain = [''] * len(key)
    for i, col in enumerate(key_order):
        plain[col] = ciphertext[i::len(key)]
    return ''.join(plain)

def main():
    with open('cipher.txt', 'r') as file:
        cipher_text = file.read().replace('\n', '').replace('TheGiant', '')

    print("Vigenère Decryption:")
    print(vigenere_decrypt(cipher_text, "TheGiant")[:100])

    print("\nPRNG-based Decryption:")
    print(prng_decrypt(cipher_text, "TheGiant")[:100])

    print("\nAES Decryption (using derived key):")
    key = derive_key("TheGiant", b"salt")
    iv = b"0" * 16  # This is just a placeholder, in reality, you'd need the correct IV
    try:
        print(aes_decrypt(cipher_text.encode(), key, iv)[:100])
    except:
        print("AES decryption failed. This might be due to incorrect key, IV, or ciphertext format.")

    print("\nSubstitution Cipher Decryption:")
    substitution_key = "QWERTYUIOPASDFGHJKLZXCVBNM"  # This is just an example key
    print(substitution_decrypt(cipher_text.upper(), substitution_key)[:100])

    print("\nTransposition Cipher Decryption:")
    print(transposition_decrypt(cipher_text, "TheGiant")[:100])

if __name__ == "__main__":
    main()
