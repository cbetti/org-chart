""" Some convenience functions for reporting issues to the user. """


def error(topic, msg):
    """ Something that should be fixed. """
    if topic:
        print(f"        ERROR ({topic}): {msg}")
    else:
        print(f"        ERROR: {msg}")


def warn(topic, msg):
    """ Something you should consider fixing. """
    if topic:
        print(f"        WARN ({topic}): {msg}")
    else:
        print(f"        WARN: {msg}")
