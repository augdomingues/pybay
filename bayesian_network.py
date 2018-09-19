from cp_table import cp_table
from dag_network import dag_network

def join_tables(names, tables):
    ensemble = dict()
    for n, t in zip(names, tables):
        ensemble[n] = t
    return ensemble


class bayesian_network():

    def __init__(self, dag, tables):

