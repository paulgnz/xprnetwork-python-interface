from importlib.metadata import version

try:
    __version__ = version("xprpy")
except:  # NOQA: E722
    pass
