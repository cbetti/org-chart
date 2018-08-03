import os
import click

from indexer import Indexer
from validation import Validation


PEOPLE_FILE = "PEOPLE.yaml"
TEAMS_FILE = "TEAMS.yaml"


@click.command('validate')
@click.option('--datadir', default=os.getcwd())
def validate(datadir=os.getcwd()):
    """ Ensure data files are well formatted and consistent. """
    indexer = Indexer(datadir)
    indexer.load()
    indexer.index()
    validator = Validation(
        indexer.people(),
        indexer.teams(),
        indexer.peoplelist(),
        indexer.teamslist())
    validator.validate()


if __name__ == '__main__':
    validate()
