### Hosted on Github at @Toblobs
### A Synergy Studios Project

version = '1.0.7_T.0.1'

from threading import Thread
import socket
        
class GameServer:
    """The server, which creates Question objects and
       broadcasts info to clients."""

    def __init__(self):

        self.SERVER_HOST = '0.0.0.0'
        self.SERVER_PORT = 7979
        self.MY_IP = socket.gethostbyname(socket.gethostname())

        self.st = '%'
        self.s = socket.socket()

        self.max_users = 100

        self.format = 'UTF-8'

        self.client_sockets = set()

    def start(self):

        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.SERVER_HOST, self.SERVER_PORT))
        self.s.listen(self.max_users)

        print(f'[*] Binded <Server> to {self.SERVER_HOST}:{self.SERVER_PORT}')
        print(f'[*] Server Private IP Address: {self.MY_IP}')

        self.loop()

    def exit(self, error = None):

        for cs in self.client_sockets:
            cs.close()

        self.s.close()

        print(f'[*] <Server> shutdown with error: {error}')

    def send(self, cs, data):

        cs.send(data.encode(self.format))

    def intr_command(self, cs, ca, msg):

        msg_list = msg.split(self.st)

        comm = msg_list[0]
        det = msg_list[1]

        print()
        print(f'[>] Client {ca} sent comm:det {comm}:{det}')

        if comm[0] == '/':

            if comm == '/confo':
                print(f'[>] Client {ca} confirmation message received!')
                self.send(cs, f'/confo{self.st}new_client_return')

            else:
                pass

        
    def listen_for_client(self, cs, ca):

        while True:

            try:

                msg = cs.recv(1024).decode()

            except BaseException as e:

                print()
                print(f'[!] Client {ca} disconnected: {e}')
                break

            else:

                self.intr_command(cs, ca, msg)
            

    def loop(self):

        print()

        while True:

            client_socket, client_address = self.s.accept()
            print(f'[+] New Client Connected: {client_address}')

            self.client_sockets.add(client_socket)

            t = Thread(target = self.listen_for_client, args = (client_socket, client_address))
            t.daemon = True
            t.start()

        self.exit()

    
#-------------------------------------------------------------------#


class Kahoot:

    def __init__(self):

        self.gs = GameServer()

    def start(self):

        print('Setting up Kahoot..')

        print('_' * 30)
        print('-' * 30)
        print()
        
        self.gs.start()

k = Kahoot()
k.start()
