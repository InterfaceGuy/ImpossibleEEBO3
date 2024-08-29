import networkx as nx
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class MagicHypercube4D:
    def __init__(self, seed):
        self.magic_constant = 130  # Sum of each row, column, etc. in a 4x4x4x4 magic hypercube
        self.seed = seed
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

    def visualize_3d_projection_magic(self, cipher_text=None):
        pos = nx.spring_layout(self.magic_graph, dim=3)
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Draw nodes
        node_colors = ['b'] * len(self.magic_graph)
        if cipher_text:
            for i, char in enumerate(cipher_text):
                node = list(self.magic_graph.nodes())[i % len(self.magic_graph)]
                node_colors[list(self.magic_graph.nodes()).index(node)] = 'r'
        
        ax.scatter([pos[v][0] for v in self.magic_graph],
                   [pos[v][1] for v in self.magic_graph],
                   [pos[v][2] for v in self.magic_graph],
                   c=node_colors)
        
        # Draw edges
        for edge in self.magic_graph.edges():
            x = [pos[edge[0]][0], pos[edge[1]][0]]
            y = [pos[edge[0]][1], pos[edge[1]][1]]
            z = [pos[edge[0]][2], pos[edge[1]][2]]
            ax.plot(x, y, z, c='gray', alpha=0.1)
        
        plt.title("3D Projection of 4x4x4x4 Magic Hypercube with Cipher Mapping")
        plt.show()

    def get_vertex_by_value(self, value):
        """
        Find the vertex coordinates for a given magic value.
        """
        for node, node_data in self.magic_graph.nodes(data=True):
            if node_data['value'] == value:
                return node
        return None

def main():
    print("\n4x4x4x4 Magic Hypercube Analysis:")
    magic_hypercube = MagicHypercube4D("TheGiant")  # Use "TheGiant" as the seed
    
    print(f"Number of vertices in magic hypercube: {magic_hypercube.get_magic_vertex_count()}")
    print(f"Number of edges in magic hypercube: {magic_hypercube.get_magic_edge_count()}")
    
    # Load cipher text
    with open('cipher.txt', 'r') as file:
        cipher_text = file.read().replace('\n', '').strip()
    
    # Visualize 3D projection with cipher mapping
    magic_hypercube.visualize_3d_projection_magic(cipher_text)

if __name__ == "__main__":
    main()
