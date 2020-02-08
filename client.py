import socket
import sys
import pickle
import threading
import time
from clientmessages import *

gamestate = None
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_host = "localhost"
server_port = 5555
username = sys.argv[1]
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
            received = sock.recv(1024)
            gamestate = pickle.loads(received)
            print(gamestate, flush=True)

    finally:
        sock.close()

def run_game():
    while True:
        time.sleep(1)


if __name__ == "__main__":
    server_thread = threading.Thread(target=connect_to_server, args=(server_host, server_port), daemon=True)
    server_thread.start()


    run_game()