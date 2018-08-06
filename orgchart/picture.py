import os
import click

from indexer import Indexer
from orggraph import OrgGraph
from viewutils import showpicture


PEOPLE_FILE = "PEOPLE.yaml"
TEAMS_FILE = "TEAMS.yaml"


@click.command('picture')
@click.argument('structure', required=1)
@click.option('--datadir', default=os.getcwd())
def picture(structure='reporting', datadir=os.getcwd()):
    """ Render an org chart PNG image and open it.

        STRUCTURE: reporting|teams """
    indexer = Indexer(datadir)
    indexer.load()
    indexer.index()
    orggraph = OrgGraph(indexer)
    orggraph.buildgraph(structure)
    imagepath = orggraph.render()
    showpicture(imagepath)


if __name__ == '__main__':
    picture()
