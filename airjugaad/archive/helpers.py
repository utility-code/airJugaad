from pathlib import Path


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


def get_name(main_pa):
    """
    Name images before saving
    """
    imPa = Path(main_pa / "data/images")
    return Path(imPa / "lastclip.png")
