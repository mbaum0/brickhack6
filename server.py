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
        try:
            if not bcast_q.empty():
                bcast_msg = bcast_q.get()
                client.sendall(pickle.dumps(bcast_msg))
        except ConnectionResetError:
            logging.debug("{} left [{}]".format(data.name, str(data.id)))
            break

    client.close()

def broadcast_all_clients():
    while True:
        for q in client_qs:
            q.put(gamestate)
        
        time.sleep(2)


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    gamestate = GameState(100, 100, 10, 1000)
    gamestate.createBoundWalls()

    HOST, PORT = "0.0.0.0", 5555
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_qs = []
    client_threads = []

    broadcaster = threading.Thread(target=broadcast_all_clients, name="Broadcaster")
    broadcaster.daemon = True
    broadcaster.start()

    try:
        sock.bind((HOST, PORT))
        sock.listen(5)
    except Exception as e:
        raise SystemExit("F this")

    sock.setblocking(0)

    while True:
        try:
            client, ip = sock.accept()
            client.setblocking(0)
            bcast_q = queue.Queue()
            client_qs.append(bcast_q)
            t = threading.Thread(target=on_new_client, args=(client, ip, bcast_q))
            client_threads.append(t)
            t.start()
        except KeyboardInterrupt:
            logging.error("F this gracefully")
            break
        except BlockingIOError:
            pass
        except Exception as e:
            logging.error("F this hard: {e}".format(e))
            break
    
    for t in client_threads:
        t.join()
        
    
    sock.close()