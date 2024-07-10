from pythonosc import dispatcher, osc_server
import time
def print_handler(address, *args):
    print(f"Received OSC message: {address} {args}")
    time.sleep(1)

dispatcher = dispatcher.Dispatcher()
dispatcher.map("/VMC/Ext/Bone/Pos/*", print_handler)

ip = "127.0.0.1"
port = 39539

server = osc_server.BlockingOSCUDPServer((ip, port), dispatcher)
print(f"Serving on {ip}:{port}")
server.serve_forever()