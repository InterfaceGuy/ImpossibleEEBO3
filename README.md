# ImpossibleEEBO3

## Project Overview

This project revolves around the cryptographic analysis and decryption of a cipher known as "TheGiantCipher". The cipher text is believed to be encrypted using an unknown method, possibly involving a 4-dimensional magic hypercube. The key "TheGiant" is suspected to play a crucial role in the encryption/decryption process. Our goal is to explore various decryption methods and analyze the structure of the cipher to uncover its hidden message.

## Progress and Exploration

1. **Initial Analysis**:
   - Removed "TheGiant" string and newline characters from the cipher text.
   - Counted the number of characters in the cleaned cipher text.

2. **Hypercube Analysis**:
   - Implemented a 4D Hypercube class to analyze its properties.
   - Created a Magic Hypercube variant with a magic constant of 130.
   - Visualized 3D projections of both regular and magic hypercubes.

3. **Decryption Attempts**:
   - Vigenère Cipher: Attempted decryption using "TheGiant" as the key.
   - PRNG-based Decryption: Used "TheGiant" to seed a random number generator for decryption.
   - AES Decryption: Derived a key from "TheGiant" using PBKDF2 and attempted AES decryption.
   - Substitution Cipher: Tried a basic substitution cipher approach.
   - Transposition Cipher: Attempted decryption using "TheGiant" as the key for column transposition.
   - Magic Hypercube Decryption: Developed a custom method using the magic hypercube properties.

4. **Current Focus**:
   - Refining the magic hypercube decryption method.
   - Exploring ways to incorporate the hypercube structure into the decryption process.
   - Investigating the relationship between "TheGiant" key and the magic hypercube properties.

5. **Future Directions**:
   - Implement dynamic magic hypercube generation for each encryption/decryption operation.
   - Explore multi-layer decryption approaches combining multiple techniques.
   - Investigate adaptive key derivation methods to strengthen the key usage.
   - Consider quantum-resistant techniques for future-proofing the encryption method.
   - Develop hybrid approaches combining the magic hypercube method with established cryptographic algorithms.

This project continues to evolve as we explore various cryptographic techniques and their potential applications to "TheGiantCipher". Each attempt provides new insights into the structure and possible encryption methods used, guiding our ongoing research and development efforts.
