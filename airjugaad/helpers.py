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
    ims_exisitng = [x for x in imPa.iterdir()]
    ims_exisitng = [x.name for x in ims_exisitng]
    nfiles = len(ims_exisitng)

    if nfiles == 0:
        return Path(imPa / "im_1.png")
    else:
        return Path(imPa / f"im_{str(nfiles+1)}.png")
