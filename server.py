import socketserver
import pickle
import time
from gamestate import GameState

gamestate = GameState(100, 100, 10, 1000)

gamestate.createBoundWalls()

class TCPSocketHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()

        gamestate.newPlayer("default")

        while True:
            print("Sent update to client @ {}".format(self.client_address), flush=True)
            msg = pickle.dumps(gamestate)
            #self.request.sendall(self.data.upper())
            self.request.sendall(msg)
            time.sleep(1)

if __name__ == "__main__":

    HOST, PORT = "0.0.0.0", 5555

    server = socketserver.TCPServer((HOST, PORT), TCPSocketHandler)

    server.serve_forever()