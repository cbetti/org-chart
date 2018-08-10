from importlib import import_module


def loadmodulewithconfig(name, indexes, configfile):
    mod = import_module(f"modules.{name}")
    config = mod.configfromfile(configfile)
    return mod.modulefromconfig(indexes, config)
