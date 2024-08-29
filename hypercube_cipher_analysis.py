import math
from magic_hypercube_analysis import MagicHypercube4D
from collections import Counter

def load_file_content(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

def analyze_hypercube_cipher_relationships():
    # Initialize the magic hypercube
    magic_hypercube = MagicHypercube4D(seed=42)  # Using a fixed seed for reproducibility
    
    # Load the cipher text and key
    cipher_text = load_file_content('cipher.txt')
    key = load_file_content('key.txt')
    
    # Gather hypercube characteristics
    hypercube_stats = {
        "Vertex Count": magic_hypercube.get_magic_vertex_count(),
        "Edge Count": magic_hypercube.get_magic_edge_count(),
        "Magic Constant": magic_hypercube.magic_constant,
        "Dimension": 4,
        "Size per Dimension": 4,
    }
    
    # Gather cipher and key characteristics
    cipher_stats = {
        "Cipher Length": 192,  # Corrected cipher length
        "Unique Characters in Cipher": len(set(cipher_text)),
        "Key": key,
        "Key Length": len(key),
    }
    
    # Calculate characters per line
    lines = cipher_text.split('\n')
    chars_per_line = [len(line) for line in lines]
    
    # Additional derived numbers
    derived_numbers = {
        "Hypercube Total Sum": hypercube_stats["Vertex Count"] * hypercube_stats["Magic Constant"] // 4,
        "Cipher Length Factors": get_factors(cipher_stats["Cipher Length"]),
        "Cipher Length Mod Vertex Count": cipher_stats["Cipher Length"] % hypercube_stats["Vertex Count"],
        "Cipher Length Mod Edge Count": cipher_stats["Cipher Length"] % hypercube_stats["Edge Count"],
        "Cipher Length Mod Magic Constant": cipher_stats["Cipher Length"] % hypercube_stats["Magic Constant"],
        "Characters per Line": chars_per_line,
    }
    
    # Analyze character frequencies
    char_frequencies = Counter(cipher_text)
    most_common_char = char_frequencies.most_common(1)[0]
    derived_numbers["Most Common Char Frequency"] = most_common_char[1]
    
    # Print analysis results
    print("Magic Hypercube Characteristics:")
    for key, value in hypercube_stats.items():
        print(f"  {key}: {value}")
    
    print("\nCipher Characteristics:")
    for key, value in cipher_stats.items():
        print(f"  {key}: {value}")
    
    print("\nDerived Numbers and Relationships:")
    for key, value in derived_numbers.items():
        print(f"  {key}: {value}")
    
    print(f"\nMost common character: '{most_common_char[0]}' (frequency: {most_common_char[1]})")
    
    # Print information about characters per line
    print("\nCharacters per line:")
    for i, count in enumerate(derived_numbers["Characters per Line"], 1):
        print(f"  Line {i}: {count} characters")
    
    # Check for potential alignments or patterns
    check_alignments(cipher_stats["Cipher Length"], hypercube_stats, derived_numbers)

def get_factors(n):
    return [i for i in range(1, n + 1) if n % i == 0]

def check_alignments(cipher_length, hypercube_stats, derived_numbers):
    alignments = []
    
    if cipher_length % hypercube_stats["Vertex Count"] == 0:
        alignments.append(f"Cipher length is divisible by vertex count: {cipher_length} / {hypercube_stats['Vertex Count']} = {cipher_length // hypercube_stats['Vertex Count']}")
    
    if cipher_length % hypercube_stats["Edge Count"] == 0:
        alignments.append(f"Cipher length is divisible by edge count: {cipher_length} / {hypercube_stats['Edge Count']} = {cipher_length // hypercube_stats['Edge Count']}")
    
    if cipher_length % hypercube_stats["Magic Constant"] == 0:
        alignments.append(f"Cipher length is divisible by magic constant: {cipher_length} / {hypercube_stats['Magic Constant']} = {cipher_length // hypercube_stats['Magic Constant']}")
    
    if derived_numbers["Most Common Char Frequency"] in derived_numbers["Cipher Length Factors"]:
        alignments.append(f"Most common character frequency ({derived_numbers['Most Common Char Frequency']}) is a factor of cipher length")
    
    if alignments:
        print("\nPotential Alignments Found:")
        for alignment in alignments:
            print(f"  - {alignment}")
    else:
        print("\nNo obvious alignments found between cipher length and hypercube characteristics.")

if __name__ == "__main__":
    analyze_hypercube_cipher_relationships()
