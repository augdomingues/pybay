import re
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import pandas as pd

class pybay:

    def __init__(self):
        self.G = nx.DiGraph()
        self.modelstring = ""
        self.model = set()
        self.node_number = 0
        self.edge_number = 0

    def __eq__(self, other):
        """ Checks if two BNs are equal by comparing their modelstrings. """
        return self.modelstring == other.modelstring

    def __repr__(self):
        out = """Random/Generated Bayesian network
                model:
                        {}
                nodes:                          {}
                arcs:                           {}
                undirected arcs:                {}
                directed arcs:                  {}
                average markov blanket size:    {}
                average neighborhood size:      {}
                average branching factor:       {}

        generation algorithm:                   Empty
        """.format(self.modelstring, self.node_number,
                   self.edge_number, 0, self.edge_number,
                   0, 0, 0)
        return out

    def model_from_set(self):
        out = "".join(["[{}]".format(prob) for prob in self.model])
        return out

    def generate_dot(self, title="Bayesian Network"):
        write_dot(self.G, "{}.dot".format(title))

    def draw(self, title="Bayesian Network", with_labels=True):
        plt.title(title)
        pos = graphviz_layout(self.G, prog="dot")
        nx.draw(self.G, pos, with_labels=with_labels, arrows=True)
        plt.show()
        plt.clf()

    def compute_modelstring(func):
        def computation(*args, **kwargs):
            func(*args, **kwargs)
            self = args[0]
            models = set()
            for node in self.G.nodes():
                parents = []
                for other_node in self.G.nodes():
                    if other_node != node:
                        if node in self.G[other_node]:
                            parents.append(other_node)
                model = "{}".format(node)
                if parents:
                    parents = sorted(parents)
                    dependencies = ":".join(parents)
                    model += "|{}".format(dependencies)
                models.add(model)
            self.model = sorted(models)
            """ TODO: currently, we sort lexicographically. Later,
                we should sort first by tree depth, then lexicographically.
            """
            self.modelstring = self.model_from_set()
        return computation

    def model_to_network(self, model):
        self.modelstring = model
        pieces = re.findall("\[.*?\]", model) #TODO validate this
        for piece in pieces:
            piece = piece.replace("[","").replace("]","")

            # Simple parent, never a child
            if len(piece) == 1:
                self.G.add_node(piece)

            # Simple son, only one parent
            if len(piece) == 3:
                son, parent = piece.split("|")
                self.G.add_node(son)
                self.G.add_node(parent)
                self.add_edge(parent, son)

            # Complex son, multiple parents
            elif len(piece) > 3:
                son, parents = piece.split("|")
                parents = parents.split(":")
                self.G.add_node(son)
                for parent in parents:
                    self.G.add_node(parent)
                    self.add_edge(parent, son)

    @compute_modelstring
    def graph_to_network(self, nodes):
        for node in nodes:
            self.G.add_node(node)
        self.node_number = len(nodes)

    @compute_modelstring
    def remove_node(self, node):
        self.G.remove_node(node)
        self.node_number -= 1

    @compute_modelstring
    def add_node(self, node):
        self.G.add_node(node)
        self.node_number += 1

    @compute_modelstring
    def add_edge(self, frm, to):
        copy_graph = self.G.copy()
        copy_graph.add_edge(frm, to)
        if nx.is_directed_acyclic_graph(copy_graph):
            self.G.add_edge(frm, to)
            self.edge_number += 1
        else:
            print("Error: the resulting graph contains cycles.")
            SystemError(0)

    @compute_modelstring
    def remove_edge(self, frm, to):
        self.G.remove_edge(frm, to)
        self.edge_number -= 1

    def nodes(self):
        print("Nodes:")
        for node in self.G.nodes():
            print(" {}".format(node), end="")
        print()

    def edges(self):
        print("From To")
        for fr, to in self.G.edges():
            print("{}   {}".format(fr, to))

if __name__ == "__main__":
    a = pybay()
    a.graph_to_network(["A", "S", "E", "O", "R", "T"])
    print(a.modelstring)
    a.add_edge("A", "E")
    a.add_edge("S", "E")
    a.add_edge("E", "O")
    a.add_edge("E", "R")
    a.add_edge("O", "T")
    a.add_edge("R", "T")
    print(a.modelstring)

    b = pybay()
    b.model_to_network("[A][S][E|A:S][O|E][R|E][T|O:R]")
