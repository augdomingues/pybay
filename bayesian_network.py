from cp_table import cp_table
from dag_network import dag_network
import networkx as nx

class bayesian_network():

    def __init__(self, dag, tables):
        self.dag = dag
        self.__undirected_dag = dag.G.to_undirected()
        self.tables = tables

    # TODO: Make d-sep support child/gran*child nodes of v-structure
    def dsep(self, frm, to, cond_to=None):
        cond_to = [] if cond_to is None else cond_to
        for path in nx.all_simple_paths(self.__undirected_dag, source=frm, target=to):
            blocked = False
            origin_node = path[0]
            for i, curr_node in enumerate(path[1:-1], 1):
                next_node = path[i+1]
                c_in_o = curr_node in self.dag.G[origin_node]
                c_in_n = curr_node in self.dag.G[next_node]
                c_in_condition = curr_node in cond_to
                if c_in_o and c_in_n and not c_in_condition:
                    blocked = True
                elif not (c_in_o and c_in_n) and c_in_condition:
                    blocked = True
                origin_node = curr_node
            if not blocked:
                print("Path {} is open.".format(path))
                print_dsep(frm, to, cond_to)
                return False
        print("No path is open.")
        print_dsep(frm, to, cond_to)
        return True

def print_dsep(frm, to, cond_to):
    if cond_to:
        print("dsep({}, {}|{}) = False".format(frm, to,
               ",".join(cond_to)))
    else:
        print("dsep({}, {}) = False".format(frm, to))

if __name__ == "__main__":
    a = dag_network()
    a.model_to_network("[A][S][E|A:S][O|E][R|E][T|O:R]")
    c = bayesian_network(a, None)
    c.dsep("A", "E")
