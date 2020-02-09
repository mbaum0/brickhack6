import socket
import sys
import pickle
import threading
import time
import struct
import pygame as pg
from gamesettings import *
from map import add_resources
from sprites import MakeSprites
from clientmessages import *
import queue


server_host = "localhost"
server_port = 5555
username = "user"

gamestate = None
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_id = None
messageQ = queue.Queue()

def connect_to_server(host, port):
    global gamestate
    global my_id
    global messageQ
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

            if not messageQ.empty():
                msg = pickle.dumps(messageQ.get())
                length = struct.pack('!I', len(msg))
                msg = length + msg

                sock.sendall(msg)

    except ConnectionResetError:
        print("Server disconnected", flush=True)
    finally:
        sock.close()



"""
PYGAME SHITE
"""
window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Client")

def draw_grid():
    for x in range(0, WIDTH, TILESIZE):
        pg.draw.line(window, LIGHTGREY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILESIZE):
        pg.draw.line(window, LIGHTGREY, (0, y), (WIDTH, y))


def redraw_window():
    global gamestate
    global my_id
    
    sprites = MakeSprites(gamestate, str(my_id))
    window.fill(BGCOLOR)
    draw_grid()
    sprites.all_sprites.draw(window)
    pg.display.update()



""" TODO run_game
Main function to update game display based upon game state
"""
def run_game():
    global messageQ
    while True:
        redraw_window()

        for event in pg.event.get():
                if event.type == pg.QUIT:
                    window.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        window.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        messageQ.put(KeyEventMessage(Keys.UP_PRESS))
                    elif event.key == pg.K_DOWN:
                        messageQ.put(KeyEventMessage(Keys.DOWN_PRESS))
                    elif event.key == pg.K_LEFT:
                        messageQ.put(KeyEventMessage(Keys.LEFT_PRESS))
                    elif event.key == pg.K_RIGHT:
                        messageQ.put(KeyEventMessage(Keys.RIGHT_PRESS))

                if event.type == pg.KEYUP:
                    if event.key == pg.K_UP:
                        messageQ.put(KeyEventMessage(Keys.UP_RELEASE))
                    elif event.key == pg.K_DOWN:
                        messageQ.put(KeyEventMessage(Keys.DOWN_RELEASE))
                    elif event.key == pg.K_LEFT:
                        messageQ.put(KeyEventMessage(Keys.LEFT_RELEASE))
                    elif event.key == pg.K_RIGHT:
                        messageQ.put(KeyEventMessage(Keys.RIGHT_RELEASE))
                if event.type == pg.MOUSEBUTTONDOWN:
                    messageQ.put(MouseEventMessage(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], Trigger.PRESSED))
                if event.type == pg.MOUSEBUTTONUP:
                    messageQ.put(MouseEventMessage(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], Trigger.RELEASED))


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
    
    while gamestate == None:
        time.sleep(1)
    run_game()
