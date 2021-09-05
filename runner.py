import argparse as ap
import cgi
import http.server
import os
import socketserver
from functools import partial
from pathlib import Path

from airjugaad.main import *


class ServerHandler(http.server.SimpleHTTPRequestHandler):
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
        # cnt = form["the_file"].file.read()
        # fn = form["the_file"].filename
        # # with open(main_pa / f"data/recieved/{fn}", "wb+") as f:
        #     f.write(cnt)


def serve(main_path):
    """
    Local server creation. Chooses a free port and creates
    """
    handler = ServerHandler
    os.chdir(main_path)

    with socketserver.TCPServer(("", ag.p), handler) as httpd:
        print(httpd.server_address)
        # print(
        #     "Server started at localhost:"
        #     + " http://0.0.0.0:"
        #     + str(httpd.server_address[1])
        # )
        httpd.serve_forever()


previous_im, previous_text = "", ""

# Arguments
arg = ap.ArgumentParser()
arg.add_argument("-f", help="folder path", type=str, default="/home/eragon/remotedir/")
arg.add_argument("-t", help="timefor", required=False, default=2)
arg.add_argument("-p", help="port", required=False, default=8080)
arg.add_argument("-i", help="your ip address", required=True, default="192.168.1.4")
ag = arg.parse_args()
port = ag.p
ipadd = ag.i
ag.f = Path(ag.f)

start_multithreaded(partial(serve, ag.f), ag, previous_im, previous_text)
