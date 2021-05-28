from pathlib import Path
import http.server
import socketserver
import threading
from airjugaad.main import *

pa = "/media/hdd/github/airJugaad/"
timefor = 2

main_pa = Path(pa)
createIfNot(main_pa/'data')
createIfNot(Path(main_pa/'data/recieved'))
createIfNot(Path(main_pa/'data/images/'))
createIfNot(main_pa/"html")
(main_pa/"data/textclip.txt").touch()

ser = "http://0.0.0.0:8080/"
generate_sites(ser, main_pa)
create_recieved_page(main_pa)

def serve():
    """
    Local server creation. Chooses a free port and creates
    """
    handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", 8080), handler) as httpd:
        print(
            "Server started at localhost:"
            + " http://0.0.0.0:"
            + str(httpd.server_address[1])
        )
        httpd.serve_forever()

serveThread = threading.Thread(target=serve)
genThread = threading.Thread(target=regenerate_sites, args=(main_pa,ser, timefor))
serveThread.start()
genThread.start()
