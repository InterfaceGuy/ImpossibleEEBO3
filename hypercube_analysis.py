import networkx as nx
import itertools
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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
        fig = plt.figure(figsize=(12, 8), facecolor='black')
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('black')
        
        # Draw nodes
        ax.scatter([pos[v][0] for v in self.graph],
                   [pos[v][1] for v in self.graph],
                   [pos[v][2] for v in self.graph],
                   c='cyan', s=50, edgecolor='white')
        
        # Draw edges
        for edge in self.graph.edges():
            x = [pos[edge[0]][0], pos[edge[1]][0]]
            y = [pos[edge[0]][1], pos[edge[1]][1]]
            z = [pos[edge[0]][2], pos[edge[1]][2]]
            ax.plot(x, y, z, c='white', alpha=0.3)
        
        # Add labels to vertices
        for v in self.graph.nodes():
            ax.text(pos[v][0], pos[v][1], pos[v][2], v, color='white', fontsize=8)
        
        plt.title("3D Projection of 4D Hypercube", color='white')
        ax.set_axis_off()
        plt.tight_layout()
        plt.savefig('hypercube_projection.png', dpi=300, bbox_inches='tight', facecolor='black')
        plt.close()

def main():
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
    
    # Visualize 3D projection
    hypercube.visualize_3d_projection()

if __name__ == "__main__":
    main()
