import socket
import sys
import pickle
import threading
import time
import struct
from map import add_resources
from clientmessages import *

server_host = "localhost"
server_port = 5555
username = "user"

gamestate = None
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_id = None

def connect_to_server(host, port):
    try:
        # Initial connection
        print("{} {}".format(host,port), flush=True)
        sock.connect((host, port))

        # Initial server connection ConnectMessage
        connect_message = pickle.dumps(ConnectMessage(username, None))
        sock.sendall(connect_message)

        # Wait for server connection response
        received = sock.recv(1024)
        connect_message = pickle.loads(received)
        my_id = connect_message.id
        print("Sever gave us a new ID!: " + str(my_id), flush=True)

        while True:
            buf = b''
            while len(buf) < 4:
                buf += sock.recv(4 - len(buf))
            
            length = struct.unpack('!I', buf)[0]

            received = sock.recv(length)
            gamestate = pickle.loads(received)
            print(gamestate, flush=True)

    except ConnectionResetError:
        print("Server disconnected", flush=True)
    finally:
        sock.close()

""" TODO run_game
Main function to update game display based upon game state
"""
def run_game():
    while True:
        time.sleep(1)

""" MAIN
    1. Parse command line input
    2. Start thread to process all client comms
    3. Enter main function to update game state model: run_game()
"""
if __name__ == "__main__":
    # Parse command line input
    numargs = len(sys.argv)
    if numargs == 2:
        username = sys.argv[1]
    elif numargs == 3:
        username = sys.argv[1]
        server_host = sys.argv[2]
    elif numargs > 3:
        username = sys.argv[1]
        server_host = sys.argv[2]
        server_port = sys.argv[3]
    else:
        print("USAGE: {} <username> <servername> <port>".format(sys.argv[0]))
        exit()
    # Start main server thread and run the game
    server_thread = threading.Thread(target=connect_to_server, args=(server_host, server_port), daemon=True)
    server_thread.start()
    run_game()
