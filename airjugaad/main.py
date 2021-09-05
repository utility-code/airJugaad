import base64
import os
import subprocess
import threading
import time

import pyperclip

from .helpers import *


def get_clip_and_save(ag, previous_im, previous_text):
    """
    Grab images from clipboard, compare with last image, save if not the same
    """
    txt = pyperclip.paste()
    im = subprocess.run(
        ["xclip", "-selection", "clipboard", "-t", "image/png", "-o"],
        stdout=subprocess.PIPE,
    )
    outim = im.stdout

    if im.returncode == 0:
        if len(outim) > 40:
            npath = os.path.join(ag.f, "imageclip.html")
            with open(npath, "w+") as f:
                if outim != previous_im:
                    data_uri = base64.b64encode(outim).decode("utf-8")
                    img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)
                    print("saving image")
                    f.write(img_tag)

        previous_im = outim
    else:
        with open(os.path.join(ag.f, "textclip.html"), "w+") as f:
            if txt != previous_text:
                print("saving text")
                f.write("\n" + txt + "\n")
        previous_text = txt


def regenerate_sites(arguments, previous_im, previous_text):
    """
    Live regenerate the website.
    """
    while True:
        time.sleep(arguments.t)
        get_clip_and_save(arguments, previous_im, previous_text)


def start_multithreaded(serve, arguments, previous_im, previous_text):
    """
    Run server in one thread and website generator in another
    """
    serveThread = threading.Thread(target=serve)
    genThread = threading.Thread(
        target=regenerate_sites,
        args=(arguments, previous_im, previous_text),
    )
    serveThread.start()
    genThread.start()
