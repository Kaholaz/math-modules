import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def check_contain_triangles(G: nx.Graph) -> bool:
    """
    Retuns true if the graph has triangles in it, false if not.
    """
    adj = nx.to_numpy_array(G)
    three_steps = np.linalg.matrix_power(adj, 3)
    return any(three_steps[i][i] != 0 for i in range(len(three_steps)))


def check_is_tree(G: nx.Graph) -> bool:
    """
    Returns true if the graph is a tree, false if not
    """
    return nx.number_of_nodes(G) == nx.number_of_edges(G) + 1 and nx.is_connected(G)


def check_all_nodes_are_of_degree(G: nx.Graph, degree: int) -> bool:
    """
    Returns true if all nodes of the graph are of the given degree.
    """
    return all(deg == degree for _, deg in G.degree())


def draw_graphs(graphs: list[nx.Graph]) -> int:
    """
    Draws all graphs in a list of graphs. Plt.show must be called to show the graphs.
    This function returns the number of graphs drawn.
    """
    for n, graph in enumerate(graphs):
        plt.figure(n)
        nx.draw(graph)
    return n + 1
