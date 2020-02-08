import pickle
import time
import socket
import threading
import logging
from gamestate import GameState



def on_new_client(client, connection):
    ip = connection[0]
    port = connection[1]
    logging.debug("New connection from {} on {}".format(ip, port))
    data = pickle.loads(client.recv(1024))
    data.id = gamestate.newPlayer(data.name)
    logging.debug("New user created with name {}".format(data.name))
    client.sendall(pickle.dumps(data))
    
    while True:
        try:
            client.sendall(pickle.dumps(gamestate))
            time.sleep(1)
        except ConnectionResetError:
            logging.debug("{} left [{}]".format(data.name, str(data.id)))
            break

    client.close()

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    gamestate = GameState(100, 100, 10, 1000)
    gamestate.createBoundWalls()

    HOST, PORT = "0.0.0.0", 5555
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        sock.bind((HOST, PORT))
        sock.listen(5)
    except Exception as e:
        raise SystemExit("F this")

    while True:
        try:
            client, ip = sock.accept()
            threading._start_new_thread(on_new_client, (client, ip))
        except KeyboardInterrupt:
            logging.error("F this gracefully")
        except Exception as e:
            logging.error("F this hard: {e}")
    
    sock.close()