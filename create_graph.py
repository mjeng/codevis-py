
import networkx as nx
from matplotlib import pyplot as plt

'''
    input: dictionary connections
        key = function name
        values = set of names of functions that it calls
'''
def draw(connections):
    g = nx.DiGraph()        # directed graph with self-loops
    g.add_nodes_from(connections.keys())

    for key in connections:
        edges = [(key, dest) for dest in connections[key]]
        g.add_edges_from(edges)

    nx.draw(g, with_labels=True, node_size=700, node_color='w', linewidths=6)
    plt.show()

def main():
    test = {}
    test["one"] = set(["two", "three", "five"])
    test["two"] = set(["two", "one"])
    test["three"] = set()
    test["four"] = set(["one"])
    test["five"] = set(["one"])
    draw(test)

if __name__ == "__main__":
    main()