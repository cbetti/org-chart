import yaml
import fields

from autovivification import AutoVivification


def indexcontent(name, content, keys):
    """ See Indexer.index for doc. """
    index = AutoVivification()
    for record in content:
        for key in keys:
            if key in record:
                if not index[key][record[key]]:
                    index[key][record[key]] = []
                index[key][record[key]].append(record)
    index['_NAME'] = name
    return index


class Indexer:
    """ Load PEOPLE and TEAMS yamls, and index all the ways. """

    def __init__(self, datadir):
        self.datadir = datadir
        self.peoplefile = f"{datadir}/PEOPLE.yaml"
        self.teamsfile = f"{datadir}/TEAMS.yaml"
        self.peoplecontent = None
        self.teamscontent = None
        self.peopleindex = None
        self.teamsindex = None

    def loadfile(self, datafile):
        """ Validates some csv formatting stuff, returns an array of arrays
            containing csv content only (no comments or blank lines). """
        with open(datafile, 'r') as data:
            datamap = yaml.safe_load(data)
            if 'PEOPLE' in datafile:
                self.peoplecontent = datamap
            if 'TEAMS' in datafile:
                self.teamscontent = datamap

    def load(self):
        self.loadfile(self.peoplefile)
        self.loadfile(self.teamsfile)

    def checkloaded(self):
        if not (self.peoplecontent and self.teamscontent):
            raise ValueError("Files were not yet loaded.")

    def index(self):
        """ Index content every possible way. This index is used by
            everything else in this codebase.

            for each content like this sample from PEOPLE:
                [   {   name: Chris Betti,
                        manager: Emil Sit,
                        team: Quality Tools },
                    {   name: Travis Miller,
                        manager: Emil Sit,
                        team: Payments Extensibility}]
            index it like so:
                {   _NAME: PEOPLE
                    name:
                    {   Chris Betti: [ <record1 ref> ],
                        Travis Miller: [ <record2 ref> ]},
                    manager:
                    {   Emil Sit: [ <record1 ref>, <record2 ref> ]},
                    team:
                    {   Quality Tools: [ <record1 ref> ],
                        Payments Extensibility: [ <record2 ref> ]}}
            """
        self.checkloaded()

        self.peopleindex = indexcontent(
            'PEOPLE',
            self.peoplecontent,
            fields.PERSONFIELDS)

        self.teamsindex = indexcontent(
            'TEAMS',
            self.teamscontent,
            fields.TEAMFIELDS)

    def checkindexed(self):
        if not (self.peopleindex and self.teamsindex):
            raise ValueError("Content was not yet indexed.")

    def peoplelist(self):
        self.checkloaded()
        return self.peoplecontent

    def teamslist(self):
        self.checkloaded()
        return self.teamscontent

    def people(self):
        self.checkindexed()
        return self.peopleindex

    def teams(self):
        self.checkindexed()
        return self.teamsindex
