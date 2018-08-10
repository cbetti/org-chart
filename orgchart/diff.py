import os
import click

from indexer import Indexer
from configuration import DEFAULT_CONFIG_FILE, ensureconfigfile
from modules.moduleloader import loadmodulewithconfig


@click.command('diff')
@click.argument('system', required=1)
@click.option('--datadir', default=os.getcwd())
@click.option('--configfile', default=DEFAULT_CONFIG_FILE)
def diff(system='placeholder',
         datadir=os.getcwd(),
         configfile=DEFAULT_CONFIG_FILE):
    """ Compare an org chart against remote systems and generate a report.

        SYSTEM: sentry|... """
    ensureconfigfile()

    indexer = Indexer(datadir)
    indexer.load()
    indexer.index()

    module = loadmodulewithconfig(system, indexer, configfile)
    if not module.issetup():
        module.interactivesetup()
    module.retrieveinfo()
    module.analyze()
    module.reportdiff()
    module.reportexceptions()


if __name__ == '__main__':
    diff()
