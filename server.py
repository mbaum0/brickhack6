import pickle
import time
import socket
import threading
import logging
import queue
import struct
from gamestate import THE_GAMESTATE
from gamestate import GameState
from gamecontroller import update_game

"""  on_new_client
Client thread processed on server
    1.  Read client connection message to get username
    2.  Send client acceptance message with that clients new UUID
    3.  Enter main infinite processing loop
        i.  Send ONE message from the message queue
        ii. Recv ONE message from the client
            - TODO: Append message to game_updates queue

@param client         :   
@param connection     :   IP address of client
@param bcast_q        :   client outgoing message queue
@param game_updater_q :   send game updates here 
"""
def on_new_client(client, connection, bcast_q, game_updater_q):
    ip = connection[0]
    port = connection[1]
    logging.debug("New connection from {} on {}".format(ip, port))

    data = pickle.loads(client.recv(1024))
    data.id = THE_GAMESTATE.newPlayer(data.name)
    client_qs[data.id] = bcast_q
    logging.debug("New user created with name {}".format(data.name))
    client.sendall(pickle.dumps(data))
    
    while True:
        try:
            # Send the first message in the queue
            if not bcast_q.empty():
                bcast_msg = bcast_q.get()
                msg = pickle.dumps(bcast_msg)
                length = struct.pack('!I', len(msg))
                msg = length + msg
                client.sendall(msg)
            # Get a message from the user and deal with it

            buf = ""
            while len(buf) < 4:
                buf += sock.recv(4 - len(buf))
            
            length = struct.unpack('!I', buf)[0]
            client_message = pickle.loads(client.recv(length))
            game_updater_q.put((client_message, data.id))

        except (ConnectionResetError, EOFError):
            break

    logging.debug("{} left [{}]".format(data.name, str(data.id)))
    del client_qs[data.id]
    THE_GAMESTATE.remove_player(data.id)
    client.close()

""" broadcast_all_clients
Periodically add message to all clients message queues.
The message added to their queues is the game state.

@param period   :   time to wait between broadcasts
"""
def broadcast_all_clients(period):
    while True:
        for q in client_qs.keys():
            try:
                client_qs[q].put(THE_GAMESTATE)
            except KeyError:
                pass # no longer connected

        time.sleep(period)

""" MAIN
Be a server for a game
"""
if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    HOST, PORT = "0.0.0.0", 5555
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_qs = {}
    client_threads = []

    broadcaster = threading.Thread(target=broadcast_all_clients, name="Broadcaster", args=(THE_GAMESTATE.fps,))
    broadcaster.daemon = True
    broadcaster.start()

    game_updater_q = queue.Queue()
    game_updater = threading.Thread(target=update_game, name="Game Updater", args=(game_updater_q,))
    game_updater.daemon = True
    game_updater.start()

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
            t = threading.Thread(target=on_new_client, args=(client, ip, bcast_q, game_updater_q))
            client_threads.append(t)
            t.start()
        except KeyboardInterrupt:
            logging.error("Detected keyboard interrupt! Exiting application")
            break
        except BlockingIOError:
            pass
        except Exception as e:
            logging.error("F this hard: {e}".format(e))
            break

    sock.close()
