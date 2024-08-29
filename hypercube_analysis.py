import networkx as nx
import itertools
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from itertools import cycle

class Hypercube4D:
    def __init__(self):
        self.graph = self._create_4d_hypercube()
        self.vertices = list(self.graph.nodes())
        self.edges = list(self.graph.edges())

    def _create_4d_hypercube(self):
        G = nx.Graph()
        for i in range(16):
            binary = format(i, '04b')
            G.add_node(binary)
        
        for u, v in itertools.combinations(G.nodes(), 2):
            if sum(c1 != c2 for c1, c2 in zip(u, v)) == 1:
                G.add_edge(u, v)
        return G

    def get_vertex_count(self):
        return len(self.vertices)

    def get_edge_count(self):
        return len(self.edges)

    def get_degree(self):
        return nx.degree(self.graph)

    def get_shortest_path(self, start, end):
        return nx.shortest_path(self.graph, start, end)

    def get_diameter(self):
        return nx.diameter(self.graph)

    def get_clustering_coefficient(self):
        return nx.average_clustering(self.graph)

    def visualize_3d_projection(self):
        pos = nx.spring_layout(self.graph, dim=3)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        
        # Draw nodes
        ax.scatter([pos[v][0] for v in self.graph],
                   [pos[v][1] for v in self.graph],
                   [pos[v][2] for v in self.graph])
        
        # Draw edges
        for edge in self.graph.edges():
            x = [pos[edge[0]][0], pos[edge[1]][0]]
            y = [pos[edge[0]][1], pos[edge[1]][1]]
            z = [pos[edge[0]][2], pos[edge[1]][2]]
            ax.plot(x, y, z, c='r', alpha=0.5)
        
        plt.title("3D Projection of 4D Hypercube")
        plt.show()

    def map_cipher_to_vertices(self, cipher_text):
        mapped_text = {}
        for i, char in enumerate(cipher_text):
            vertex = self.vertices[i % len(self.vertices)]
            if vertex not in mapped_text:
                mapped_text[vertex] = []
            mapped_text[vertex].append(char)
        return mapped_text

class MagicHypercube4D(Hypercube4D):
    def __init__(self, seed):
        super().__init__()
        self.magic_constant = 130  # Sum of each row, column, etc. in a 4x4x4x4 magic hypercube
        self.magic_graph = self._create_magic_4d_hypercube(seed)

    def _create_magic_4d_hypercube(self, seed):
        random.seed(seed)
        G = nx.Graph()
        values = list(range(1, 257))
        random.shuffle(values)
        
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    for l in range(4):
                        value = values.pop()
                        G.add_node((i, j, k, l), value=value)
        
        # Connect nodes that differ in only one coordinate
        for node in G.nodes():
            for dim in range(4):
                for offset in [-1, 1]:
                    neighbor = list(node)
                    neighbor[dim] = (neighbor[dim] + offset) % 4
                    G.add_edge(node, tuple(neighbor))
        
        return G

    def get_vertex_value(self, vertex):
        return self.magic_graph.nodes[vertex]['value']

    def get_magic_vertex_count(self):
        return len(self.magic_graph.nodes())

    def get_magic_edge_count(self):
        return len(self.magic_graph.edges())

    def visualize_3d_projection_magic(self):
        pos = nx.spring_layout(self.magic_graph, dim=3)
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Draw nodes
        ax.scatter([pos[v][0] for v in self.magic_graph],
                   [pos[v][1] for v in self.magic_graph],
                   [pos[v][2] for v in self.magic_graph])
        
        # Draw edges
        for edge in self.magic_graph.edges():
            x = [pos[edge[0]][0], pos[edge[1]][0]]
            y = [pos[edge[0]][1], pos[edge[1]][1]]
            z = [pos[edge[0]][2], pos[edge[1]][2]]
            ax.plot(x, y, z, c='r', alpha=0.1)
        
        plt.title("3D Projection of 4x4x4x4 Magic Hypercube")
        plt.show()

    def map_cipher_to_magic_vertices(self, cipher_text):
        mapped_text = {}
        magic_vertices = list(self.magic_graph.nodes())
        for i, char in enumerate(cipher_text):
            vertex = magic_vertices[i % len(magic_vertices)]
            if vertex not in mapped_text:
                mapped_text[vertex] = []
            mapped_text[vertex].append(char)
        return mapped_text


def main():
    # Count cipher letters
    with open('cipher.txt', 'r') as file:
        cipher_text = file.read().replace('\n', '').replace('TheGiant', '')
    cipher_length = len(cipher_text)
    print(f"Number of letters in the cipher: {cipher_length}")

    print("\nRegular 4D Hypercube Analysis:")
    hypercube = Hypercube4D()
    
    print(f"Number of vertices: {hypercube.get_vertex_count()}")
    print(f"Number of edges: {hypercube.get_edge_count()}")
    print(f"Degree of each vertex: {list(hypercube.get_degree())[0][1]}")
    print(f"Diameter of the hypercube: {hypercube.get_diameter()}")
    print(f"Average clustering coefficient: {hypercube.get_clustering_coefficient()}")
    
    # Example of finding shortest path
    start, end = '0000', '1111'
    path = hypercube.get_shortest_path(start, end)
    print(f"Shortest path from {start} to {end}: {' -> '.join(path)}")
    
    print("\n4x4x4x4 Magic Hypercube Analysis:")
    magic_hypercube = MagicHypercube4D()
    
    print(f"Number of vertices in magic hypercube: {magic_hypercube.get_magic_vertex_count()}")
    print(f"Number of edges in magic hypercube: {magic_hypercube.get_magic_edge_count()}")
    
    # Map cipher text to vertices
    with open('cipher.txt', 'r') as file:
        cipher_text = file.read().replace('\n', '').replace('TheGiant', '')
    
    mapped_text = magic_hypercube.map_cipher_to_magic_vertices(cipher_text)
    print("\nMapping of cipher text to magic hypercube vertices:")
    for vertex, chars in mapped_text.items():
        print(f"{vertex}: {''.join(chars)}")
    
    # Visualize 3D projections
    hypercube.visualize_3d_projection()
    magic_hypercube.visualize_3d_projection_magic()


if __name__ == "__main__":
    main()
