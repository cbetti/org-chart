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
@click.option('--engine', default='dot')
@click.option('--teammembers/--no-teammembers', default=True)
@click.option('--openimage/--no-openimage', default=True)
def picture(structure='reporting', datadir=os.getcwd(), engine='dot',
            teammembers=True, openimage=True):
    """ Render an org chart PNG image and open it.

        STRUCTURE: reporting|teams """
    indexer = Indexer(datadir)
    indexer.load()
    indexer.index()
    orggraph = OrgGraph(indexer, engine, teammembers)
    orggraph.buildgraph(structure)
    imagepath = orggraph.render()
    if openimage:
        showpicture(imagepath)


if __name__ == '__main__':
    picture()
