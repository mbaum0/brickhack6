import socket
import sys
import pickle
import threading
import time

gamestate = None
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_host = "localhost"
server_port = 5555

def connect_to_server(host, port):
    try:
        print("{} {}".format(host,port), flush=True)
        sock.connect((host, port))
        
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