import unicodedata
import re

from shutil import which
from graphviz import Digraph


def checkstructure(structuretype):
    if structuretype not in ['reporting', 'teams']:
        raise ValueError("'reporting' and 'teams' are the only supported "
                         "structures at this time")


def checkgraphviz(engine):
    if not which(engine):
        raise SystemError(f"{engine} binary not found, please adjust "
                          "path or install graphviz")


def slugify(value):
    """ Normalizes string, converts to lowercase, removes non-alpha characters,
        and converts spaces to hyphens. Adapted from Django. """
    value = unicodedata.normalize('NFKD', value)\
        .encode('ascii', 'ignore')\
        .decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '_', value)


def clustername(humanfriendlyname):
    return 'cluster_' + slugify(humanfriendlyname)


class OrgGraph:

    def __init__(self, indexes, engine, teammembers):
        self.indexes = indexes
        self.engine = engine
        self.includeindividualsinteams = teammembers
        self.graph = None

    def buildreportinggraph(self):
        graph = Digraph(format='png', engine=self.engine)
        for person in self.indexes.peoplecontent:
            graph.node(person['name'])
            if 'manager' in person:
                graph.edge(person['manager'], person['name'])
        return graph

    def buildteamsgraph(self):
        graph = Digraph(format='png', engine=self.engine)
        graph.attr(compound='true')
        # graph.attr(splines='ortho')
        for team in self.indexes.teamscontent:
            self.buildteam(graph, team)
        self.buildteamhierarchy(graph)
        self.completeteamreportingstructure(graph)
        return graph

    def buildteam(self, graph, team):
        with graph.subgraph(name=clustername(team['team'])) as tgraph:
            tgraph.attr(color='blue')
            tgraph.attr(label=team['team'])
            tgraph.attr(rank='same')
            # We need a guaranteed-present node to point to within the team,
            # so we introduce an invisible node. However, it occupies space,
            # and width=0, length=0 doesn't help. An alternate approach would
            # be to deterministically choose a visible node, which could be
            # this space-occupying invisible node if there is no visible node.
            tgraph.node(team['team'], style='invis')
            self.buildteamprincipals(tgraph, team)

    def buildteamprincipals(self, tgraph, team):
        prevnode = team['team']
        leads = self.indexes.peopleindex['name'].get(team['lead'])
        if leads and leads[0]:
            leadname = leads[0]['name']
            # One person can lead more than one team, so we must distinguish or
            # dot will not render all of them.
            leadnode = leadname + '__' + team['team']
            tgraph.node(leadnode, label=leadname, shape='egg')
            tgraph.edge(team['team'], leadnode, style='invis')
            prevnode = leadnode
        self.buildteamindividuals(tgraph, team, leads[0], prevnode)

    def buildteamindividuals(self, tgraph, team, lead, prevnode):
        if not self.includeindividualsinteams:
            return
        for person in self.indexes.peopleindex['team'][team['team']]:
            if lead and person['name'] == lead['name']:
                continue
            tgraph.node(person['name'], shape='box')
            tgraph.edge(prevnode, person['name'], style='invis')
            prevnode = person['name']

    def buildteamhierarchy(self, graph):
        for team in self.indexes.teamscontent:
            if team.get('part of'):
                graph.edge(team['part of'], team['team'],
                           ltail=clustername(team['part of']),
                           lhead=clustername(team['team']))

    def completeteamreportingstructure(self, graph):
        """ At some point teams aren't part of teams, so we switch to rendering
            the PEOPLE reporting hierarchy all the way to the top. """
        edges = set()
        for team in self.indexes.teamscontent:
            boss = team.get('reporting to')
            if not team.get('part of') and boss:
                graph.edge(boss, team['team'], lhead=clustername(team['team']))
                self.completepersonreportingstructure(
                    graph,
                    self.indexes.peopleindex['name'][boss][0],
                    edges)

    def completepersonreportingstructure(self, graph, person, edges):
        """ We assume the person passed in is already a node in graph. We
            eliminate duplicate edges by short-circuiting if we already know
            about the edge. """
        boss = person.get('manager')
        if not boss:
            return
        edgekey = person['name'] + '__' + boss
        if edgekey in edges:
            return
        graph.edge(boss, person['name'])
        edges.add(edgekey)
        self.completepersonreportingstructure(  # recursion
            graph,
            self.indexes.peopleindex['name'][boss][0],
            edges)

    def buildgraph(self, structuretype):
        checkstructure(structuretype)
        if structuretype == 'reporting':
            self.graph = self.buildreportinggraph()
        elif structuretype == 'teams':
            self.graph = self.buildteamsgraph()

    def checkgraphed(self):
        if not self.graph:
            raise ValueError("Org was not yet graphed.")

    def render(self):
        self.checkgraphed()
        checkgraphviz(self.engine)
        imagepath = 'graphviz-orgchart'
        self.graph.render(imagepath)
        return imagepath + '.png'
