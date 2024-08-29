from magic_hypercube_analysis import MagicHypercube4D

class MagicHypercubeDecryption:
    @staticmethod
    def map_cipher_to_vertices(cipher_text, vertices):
        mapped_text = {}
        for i, char in enumerate(cipher_text):
            vertex = vertices[i % len(vertices)]
            if vertex not in mapped_text:
                mapped_text[vertex] = []
            mapped_text[vertex].append(char)
        return mapped_text

    @staticmethod
    def decrypt_with_magic_hypercube(cipher_text, magic_hypercube, mapping_strategy='default'):
        """
        Decrypt the cipher text using the magic hypercube structure with various mapping strategies.
        """
        magic_vertices = list(magic_hypercube.magic_graph.nodes())
        
        if mapping_strategy == 'reverse':
            magic_vertices.reverse()
        elif mapping_strategy == 'descending':
            magic_vertices = sorted(magic_vertices, key=lambda x: (x[0], x[1], x[2], x[3]), reverse=True)
        elif mapping_strategy == 'ascending':
            magic_vertices = sorted(magic_vertices, key=lambda x: (x[0], x[1], x[2], x[3]))
        elif mapping_strategy == 'value_ascending':
            magic_vertices = sorted(magic_vertices, key=lambda x: magic_hypercube.get_vertex_value(x))
        elif mapping_strategy == 'value_descending':
            magic_vertices = sorted(magic_vertices, key=lambda x: magic_hypercube.get_vertex_value(x), reverse=True)
        
        mapped_values = MagicHypercubeDecryption.map_cipher_to_vertices(cipher_text, magic_vertices)
        decrypted_text = ""
        
        for vertex, chars in mapped_values.items():
            for char in chars:
                x, y, z, w = vertex
                magic_value = magic_hypercube.get_vertex_value(vertex)
                shift = (x + y + z + w + magic_value) % 26
                char_value = (ord(char) - 65 - shift) % 26
                decrypted_text += chr(char_value + 65)
        
        return decrypted_text

def main():
    # Read cipher text
    with open('cipher.txt', 'r') as file:
        cipher_text = file.read()
    
    print(f"Total characters in the file (including newlines): {len(cipher_text)}")
    print(f"Cipher text (raw):\n{repr(cipher_text)}")
    
    # Strip whitespace and count again
    cipher_text = cipher_text.strip()
    print(f"\nTotal characters after stripping whitespace: {len(cipher_text)}")
    print(f"Cipher text (stripped):\n{repr(cipher_text)}")
    
    # Remove 'TheGiant' and count again
    processed_cipher = cipher_text.replace('TheGiant', '')
    print(f"\nTotal characters after removing 'TheGiant': {len(processed_cipher)}")
    print(f"Processed cipher:\n{repr(processed_cipher)}")
    
    # Count only letters
    letter_count = sum(c.isalpha() for c in processed_cipher)
    print(f"\nNumber of letters in the processed cipher: {letter_count}")

    # Create a real magic hypercube
    magic_hypercube = MagicHypercube4D("TheGiant")

    # Decrypt using magic hypercube with different mapping strategies
    mapping_strategies = ['default', 'reverse', 'descending', 'ascending', 'value_ascending', 'value_descending']
    
    for strategy in mapping_strategies:
        decrypted_text = MagicHypercubeDecryption.decrypt_with_magic_hypercube(processed_cipher, magic_hypercube, strategy)
        print(f"\nDecrypted text using {strategy} mapping strategy:")
        print(decrypted_text[:100] + "...")  # Print first 100 characters

if __name__ == "__main__":
    main()
