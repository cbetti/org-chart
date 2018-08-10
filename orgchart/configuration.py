import os

DEFAULT_HOME_DIR = os.path.expanduser("~/.orgchart")
DEFAULT_CONFIG_FILE = DEFAULT_HOME_DIR + "/config.ini"


def ensurehomedir():
    if not os.path.exists(DEFAULT_HOME_DIR):
        os.mkdir(DEFAULT_HOME_DIR)


def ensureconfigfile():
    ensurehomedir()
    if not os.path.exists(DEFAULT_CONFIG_FILE):
        with open(DEFAULT_CONFIG_FILE, 'a'):
            os.utime(DEFAULT_CONFIG_FILE, None)
