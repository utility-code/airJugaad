import argparse as ap
from functools import partial
from pathlib import Path

from airjugaad.main import *

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

# actual execution
create_reqs(ag.f)
start_multithreaded(partial(serve, ag), ag, previous_im, previous_text)
