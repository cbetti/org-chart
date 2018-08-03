import fields

from output import error, warn


def extraneousfields(itemlist, listname, knownfields):
    for record in itemlist:
        for key in record:
            if key not in knownfields:
                warn(listname, f"found extraneous field '{key}', typo?")


def checkdupes(index, field):
    if field not in fields.PERSONFIELDS and \
       field not in fields.TEAMFIELDS:
        raise ValueError(f"checking unrecognized field '{field}'")

    dupes = set()
    for key, value in index[field].items():
        if len(value) > 1:
            dupes.add(key)
    if dupes:
        error(index['_NAME'],
              f"duplicate {field}(s) found: {', '.join(sorted(dupes))}")


def allpresentin(index, field, targetindex, targetfield):
    if field not in fields.PERSONFIELDS and \
       field not in fields.TEAMFIELDS:
        raise ValueError(f"checking unrecognized field '{field}'")
    if targetfield not in fields.PERSONFIELDS and \
       targetfield not in fields.TEAMFIELDS:
        raise ValueError(f"checking unrecognized targetfield '{targetfield}'")

    tracker = {}
    for key in index[field]:
        tracker[key] = 1
    for key in targetindex[targetfield]:
        tracker[key] = tracker.get(key, 0) - 1
    notfound = list(filter(lambda key: tracker[key] > 0, tracker))
    if notfound:
        error(None, "{0}[{1}(s)] not found in {2}[{3}]: {4}".format(
            index['_NAME'], field, targetindex['_NAME'], targetfield,
            ', '.join(sorted(notfound))))


def checkmissing(itemlist, listname, field, identifybyfield):
    missing = set()
    for record in itemlist:
        if field not in record:
            missing.add(record[identifybyfield])
    if missing:
        warn(listname, f"missing {field} for: {', '.join(sorted(missing))}")


class Validation:
    """ Ensure data files are well formatted and consistent. """

    def __init__(self, peopleindex, teamsindex, peoplecontent, teamscontent):
        self.peopleindex = peopleindex
        self.teamsindex = teamsindex
        self.peoplecontent = peoplecontent
        self.teamscontent = teamscontent

    def validate(self):
        self.fields()
        self.consistency()
        self.missinginfo()

    def fields(self):
        extraneousfields(self.peoplecontent, 'PEOPLE', fields.PERSONFIELDS)
        extraneousfields(self.teamscontent, 'TEAMS', fields.TEAMFIELDS)

    def consistency(self):
        checkdupes(self.peopleindex, 'name')
        checkdupes(self.peopleindex, 'email')
        checkdupes(self.peopleindex, 'slack handle')
        checkdupes(self.teamsindex, 'team')
        checkdupes(self.teamsindex, 'team email')
        checkdupes(self.teamsindex, 'public slack channel')
        allpresentin(self.peopleindex, 'manager',
                     self.peopleindex, 'name')
        allpresentin(self.teamsindex, 'lead',
                     self.peopleindex, 'name')
        allpresentin(self.teamsindex, 'reporting to',
                     self.peopleindex, 'name')
        allpresentin(self.peopleindex, 'team',
                     self.teamsindex, 'team')

    def missinginfo(self):
        checkmissing(self.peoplecontent, 'PEOPLE', 'email', 'name')
        checkmissing(self.peoplecontent, 'PEOPLE', 'slack handle', 'name')
        checkmissing(self.teamscontent, 'TEAMS', 'slack handle', 'team')
