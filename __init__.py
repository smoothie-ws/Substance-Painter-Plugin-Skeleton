from .src.plugin import Plugin, Path


def start_plugin():
    Plugin.start(Path.to(__file__))


def close_plugin():
    Plugin.close()
