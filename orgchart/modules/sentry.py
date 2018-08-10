import configparser
import requests

from output import error, warn


CONFIG_SECTION = 'sentry'
CONFIG_CLASS = 'SentryModuleConfig'
MODULE_CLASS = 'SentryModule'
NO_AUTH_TOKEN_MSG = """
ERROR: No sentry auth token found in {configfile}

You can find or create a sentry API token for your user here:

    https://sentry.io/settings/account/api/auth-tokens/
"""
NO_ORGANIZATION_MSG = """
ERROR: No sentry organization slug found in {configfile}

You can find your organization's slug in your org's sentry web URL. For
example, if your organization is Toast, the slug is toast:

    https://sentry.io/toast/
"""


def configfromfile(configfile):
    configcontent = configparser.ConfigParser()
    configcontent.read(configfile)
    config = SentryModuleConfig(configfile)
    if CONFIG_SECTION in configcontent:
        section = configcontent[CONFIG_SECTION]
        config.auth_token = section.get('auth_token')
        config.organization = section.get('organization')
    return config


def sentryrequest(headers, url):
    req = requests.get(url, headers=headers)
    if req.status_code != requests.codes.ok:
        raise Exception(f"bad sentry response: {req.json().get('detail')}")
    return req.json()


class SentryModuleConfig:
    """ Organization Slug, Token, etc. for communicating with Sentry. """

    def __init__(self, configfile):
        self.configfile = configfile
        self.auth_token = None
        self.organization = None

    def writeconfigsection(self):
        section = {
            'auth_token': self.auth_token,
            'organization': self.organization,
            }
        config = configparser.ConfigParser()
        config.read(self.configfile)
        config[CONFIG_SECTION] = section
        with open(self.configfile, 'w') as configout:
            config.write(configout)

    def interactivesetupauthtoken(self):
        print(NO_AUTH_TOKEN_MSG.format(configfile=self.configfile))
        answer = input('What is your token? ')
        self.auth_token = answer
        self.writeconfigsection()

    def interactivesetuporganization(self):
        print(NO_ORGANIZATION_MSG.format(configfile=self.configfile))
        answer = input('What is your organization slug? ')
        self.organization = answer
        self.writeconfigsection()


def modulefromconfig(indexes, config: SentryModuleConfig):
    return SentryModule(indexes, config)


class SentryModule:
    """ Checks Sentry for consistency with orgchart. """

    def __init__(self, indexes, config: SentryModuleConfig):
        self.indexes = indexes
        self.config = config
        self.client = None
        self.sentryteams = None
        self.sentrymembers = None
        self.missingteamslug = []
        self.missingteams = []
        self.missingmemberslug = []
        self.missingmembers = []

    def issetup(self):
        return self.config.auth_token and self.config.organization

    def interactivesetup(self):
        if not self.config.auth_token:
            self.config.interactivesetupauthtoken()
        if not self.config.organization:
            self.config.interactivesetuporganization()

    def diffteammembership(self, team):
        pass

    def retrieveinfo(self):
        headers = {'Authorization': f'Bearer {self.config.auth_token}'}
        teams_url = 'https://sentry.io/api/0/organizations/'\
            f'{self.config.organization}/teams/'
        members_url = 'https://sentry.io/api/0/organizations/'\
            f'{self.config.organization}/members/'

        self.sentryteams = sentryrequest(headers, teams_url)
        self.sentrymembers = sentryrequest(headers, members_url)

    def analyze(self):
        for team in self.indexes.teamscontent:
            self.analyzeteam(team)
        for person in self.indexes.peoplecontent:
            self.analyzeperson(person)

    def analyzeteam(self, team):
        slug = team.get('sentry team slug')
        if not slug:
            self.missingteamslug.append(
                f"'{team['team']}' does not have a sentry team slug defined")
        elif slug not in list(map(
                lambda steam: steam['slug'], self.sentryteams)):
            self.missingteams.append(
                "'{team}' team sentry slug not found in sentry: {slug}".format(
                    team=team['team'],
                    slug=slug))

    def analyzeperson(self, person):
        slug = person.get('sentry user slug')
        if not slug:
            self.missingmemberslug.append(
                f"'{person['name']}' does not have a sentry user slug defined")
        elif slug not in list(map(
                lambda smember: smember['name'], self.sentrymembers)):
            self.missingmembers.append(
                "'{person}'s user slug not found in sentry: {slug}".format(
                    person=person['name'],
                    slug=slug))

    def reportdiff(self):
        pass

    def reportexceptions(self):
        for msg in self.missingmemberslug:
            warn('sentry', msg)
        for msg in self.missingteamslug:
            warn('sentry', msg)
        for msg in self.missingmembers:
            error('sentry', msg)
        for msg in self.missingteams:
            error('sentry', msg)
