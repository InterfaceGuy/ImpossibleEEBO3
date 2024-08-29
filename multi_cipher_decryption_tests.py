import random
import string
from itertools import cycle
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from hypercube_analysis import MagicHypercube4D

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

def magic_hypercube_decrypt(ciphertext, key):
    # Generate a seed from the key
    seed = sum(ord(c) for c in key)
    
    # Create the magic hypercube
    hypercube = MagicHypercube4D(seed)
    
    # Map characters to vertices
    vertices = list(hypercube.magic_graph.nodes())
    char_to_vertex = {c: vertices[i % len(vertices)] for i, c in enumerate(set(ciphertext))}
    
    decrypted = []
    for char in ciphertext:
        vertex = char_to_vertex[char]
        value = hypercube.get_vertex_value(vertex)
        
        # Use the magic constant and vertex value to decrypt
        decrypted_ord = (ord(char) - value + hypercube.magic_constant) % 256
        decrypted.append(chr(decrypted_ord))
    
    return ''.join(decrypted)

def run_multi_cipher_tests():
    with open('cipher.txt', 'r') as file:
        cipher_text = file.read().replace('\n', '').replace('TheGiant', '')

    decryption_methods = [
        ("Vigenère", lambda: vigenere_decrypt(cipher_text, "TheGiant")),
        ("PRNG-based", lambda: prng_decrypt(cipher_text, "TheGiant")),
        ("AES", lambda: aes_decrypt(cipher_text.encode(), derive_key("TheGiant", b"salt"), b"0" * 16)),
        ("Substitution", lambda: substitution_decrypt(cipher_text.upper(), "QWERTYUIOPASDFGHJKLZXCVBNM")),
        ("Transposition", lambda: transposition_decrypt(cipher_text, "TheGiant")),
        ("Magic Hypercube", lambda: magic_hypercube_decrypt(cipher_text, "TheGiant"))
    ]

    for method_name, decrypt_func in decryption_methods:
        print(f"\n{method_name} Decryption:")
        try:
            decrypted = decrypt_func()
            print(decrypted[:100])
        except Exception as e:
            print(f"Decryption failed: {str(e)}")

if __name__ == "__main__":
    run_multi_cipher_tests()
