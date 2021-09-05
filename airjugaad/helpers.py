from .helpers import *


def iseq(x, y):
    """
    Test for equality
    """
    return x == y


def createIfNot(x):
    """
    If path does not exist -> create
    else leave it as it is
    """
    Path.mkdir(x, exist_ok=True)
