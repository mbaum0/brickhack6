import pickle
import time
import socket
import threading
import logging
import queue
from gamestate import GameState

def on_new_client(client, connection, bcast_q):
    ip = connection[0]
    port = connection[1]
    logging.debug("New connection from {} on {}".format(ip, port))
    data = pickle.loads(client.recv(1024))
    data.id = gamestate.newPlayer(data.name)
    logging.debug("New user created with name {}".format(data.name))
    client.sendall(pickle.dumps(data))
    
    while True:
        # Send the first message in the queue
        try:
            if not bcast_q.empty():
                bcast_msg = bcast_q.get()
                client.sendall(pickle.dumps(bcast_msg))
        except ConnectionResetError:
            logging.debug("{} left [{}]".format(data.name, str(data.id)))
            break
        # Get a message from the user and deal with it
        try:
            client_message = pickle.loads(client.recv(1024))
            if(isinstance(client_message, MouseEventMessage)):
                mouseEventUpdate(client_message, data.id)
            elif(isinstance(client_message, KeyEventMessage)):
                keyEventUpdate(client_message, data.id)
            else:
                logging.debug("{} left [{}]".format(data.name, str(data.id)))
                break
        except BlockingIOError:
            logging.debug("No message from client.. but thats ok")

    client.close()

def broadcast_all_clients(name):
    for q in clients:
        q.put(gamestate)
    
    time.sleep(2)


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    gamestate = GameState(100, 100, 10, 1000)
    gamestate.createBoundWalls()

    HOST, PORT = "0.0.0.0", 5555
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    clients = []

    threading._start_new_thread(broadcast_all_clients, ("broadcaster",))

    try:
        sock.bind((HOST, PORT))
        sock.listen(5)
    except Exception as e:
        raise SystemExit("F this")

    while True:
        try:
            client, ip = sock.accept()
            client.setblocking(0)
            bcast_q = queue.Queue()
            clients.append(bcast_q)
            threading._start_new_thread(on_new_client, (client, ip, bcast_q))
        except KeyboardInterrupt:
            logging.error("Detected keyboard interrupt! Exiting application")
            break
        except Exception as e:
            logging.error("F this hard: {e}")
    
    sock.close()
