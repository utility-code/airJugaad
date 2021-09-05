import subprocess
import threading
import time
from pathlib import Path

import pyperclip

from .backbone import *
from .helpers import *

previous_text = ""
previous_im = ""


def execute_functions(
    serve,
    regenerate_sites,
    main_pa,
    ser,
    ser2,
    timefor,
    index_html,
    index_html2,
    index_html3,
    form_sr,
    ag,
):
    """
    initialize the directory, start the application
    """
    initialize(index_html, index_html2, main_pa, ser2, ser, form_sr, timefor)

    start_multithreaded(
        serve, regenerate_sites, main_pa, ser, timefor, index_html, index_html2, ag
    )


def get_clip_and_save(main_pa):
    """
    Grab images from clipboard, compare with last image, save if not the same
    """
    global previous_im
    global previous_text
    txt = pyperclip.paste()
    im = subprocess.run(
        ["xclip", "-selection", "clipboard", "-t", "image/png", "-o"],
        stdout=subprocess.PIPE,
    )
    outim = im.stdout

    if im.returncode == 0:
        if len(outim) > 40:
            with open(get_name(main_pa), "wb+") as f:
                if outim != previous_im:
                    print("saving image")
                    f.write(outim)
        previous_im = outim
    else:
        with open(main_pa / "data/textclip.txt", "a+") as f:
            if txt != previous_text:
                print("saving text")
                f.write("\n" + txt + "\n")
        previous_text = txt


def start_multithreaded(
    serve, regenerate_sites, main_pa, ser, timefor, index_html, index_html2, ag
):
    """
    Run server in one thread and website generator in another
    """
    serveThread = threading.Thread(target=serve)
    ser2 = f"http://{str(ag.i)}:{str(ag.p)}/"
    genThread = threading.Thread(
        target=regenerate_sites,
        args=(main_pa, ser, ser2, timefor, index_html, index_html2),
    )
    serveThread.start()
    genThread.start()


def regenerate_sites(main_pa, ser, ser2, waitfor, index_html, index_html2):
    """
    Live regenerate the website.
    """
    while True:
        time.sleep(waitfor)
        get_clip_and_save(main_pa)
        generate_sites(index_html, index_html2, main_pa, ser2, ser, waitfor)


def initialize(index_html, index_html2, main_pa, ser2, ser, form_sr, waitfor):
    """
    Set up needed directories, create files etc
    """
    createIfNot(main_pa / "data")
    createIfNot(Path(main_pa / "data/recieved/"))
    createIfNot(Path(main_pa / "data/images/"))
    createIfNot(main_pa / "html")
    (main_pa / "data/textclip.txt").touch()
    generate_sites(index_html, index_html2, main_pa, ser2, ser, waitfor)
    create_recieved_page(main_pa, form_sr)
