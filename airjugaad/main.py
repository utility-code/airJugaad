import base64
import cgi
import cgitb

cgitb.enable()
import http.server
import os
import socketserver
import subprocess
import threading
import time
from pathlib import Path

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


def create_reqs(main_path):
    """
    Create the paths that are required
    """
    Path.mkdir(main_path / "data", exist_ok=True)
    with open(main_path / "index.html", "w+") as f:
        f.write(
            """
        <html>
<body>
   <form enctype = "multipart/form-data" method = "post">
   <p>File: <input type = "file" name = "filename" /></p>
   <p><input type = "submit" value = "Upload" /></p>
</form>
</body>
</html>
            """
        )


class ServerHandler(http.server.SimpleHTTPRequestHandler):
    """
    Class to handle the server functions
    """

    def do_GET(self):
        http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                "REQUEST_METHOD": "POST",
                "CONTENT_TYPE": self.headers["Content-Type"],
            },
        )
        http.server.SimpleHTTPRequestHandler.do_GET(self)

        fileitem = form["filename"]
        if fileitem.filename:
            fn = os.path.basename(fileitem.filename)
            open("data/" + fn, "wb").write(fileitem.file.read())
            message = 'The file "' + fn + '" was uploaded successfully'
        else:
            message = "No file was uploaded"
        print(
            """\
            Content-Type: text/html\n
            <html>
            <body>
            <p>%s</p>
            </body>
            </html>
            """
            % (message,)
        )


def serve(ag):
    """
    Local server creation. Chooses a free port and creates
    """
    handler = ServerHandler
    os.chdir(ag.f)

    with socketserver.TCPServer(("", ag.p), handler) as httpd:
        print(httpd.server_address)
        httpd.serve_forever()
