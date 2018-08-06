from shutil import which
from graphviz import Digraph


def checkstructure(structuretype):
    if structuretype not in ['reporting']:
        raise ValueError("'reporting' is the only supported structure "
                         "at this time")


def checkgraphviz():
    if not which('dot'):
        raise SystemError("'dot' binary not found, please adjust "
                          "path or install graphviz")


# class Edge:
#
#    def __init__(self, source, target):
#        self.source = source
#        self.target = target
#
#
class OrgGraph:

    def __init__(self, indexes):
        self.indexes = indexes
        self.graph = None

    def buildreportinggraph(self):
        dot = Digraph(format='png')
        for person in self.indexes.peoplecontent:
            dot.node(person['name'])
            if 'manager' in person:
                dot.edge(person['manager'], person['name'])
        return dot

    def buildgraph(self, structuretype):
        checkstructure(structuretype)
        if structuretype == 'reporting':
            self.graph = self.buildreportinggraph()

    def checkgraphed(self):
        if not self.graph:
            raise ValueError("Org was not yet graphed.")

    def render(self):
        self.checkgraphed()
        checkgraphviz()
        imagepath = 'graphviz-orgchart'
        self.graph.render(imagepath)
        return imagepath + '.png'
