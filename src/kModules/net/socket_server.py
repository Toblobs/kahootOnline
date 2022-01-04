### Hosted on Github at @Toblobs
### A Synergy Studios Project

import socket
from .packet import Packet

from threading import Thread

class SocketServer:

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
        self.client_addr = {}

        self.names = {}

        self.question_queue = []
        self.question_queue_change = False

        self.state = None

    def start_server(self):

        """Starts the server and prints out info,
           then starts the loop."""

        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.SERVER_HOST, self.SERVER_PORT))
        self.s.listen(self.max_users)

        print(f'[*] Binded <Server> to {self.SERVER_HOST}:{self.SERVER_PORT}')
        print(f'[*] Server Private IP Address: {self.MY_IP}')

        self.loop()

    def exit_server(self, error = None):

        """Exits the server with an optional error."""

        for cs in self.client_sockets:
            cs.close()

        self.s.close()

        print(f'[*] <Server> shutdown with error: {error}')

    def send(self, cs, packet):

        """Sends data to the client as encoded in the specified format."""

        cs.send(packet.unwrap(self.st).encode(self.format))

    def broadcast(self, to, packet):

        """Broadcasts the data to a select no. of clients in our list,"""

        if to == 'all':

            for cs in self.client_sockets:
                cs.send(packet.unwrap(self.st).encode(self.format))

    def intr_command(self, cs, packet):

        """Handldes commands from the message defined
           and prints out the various info."""

        ca = self.client_addr[cs]

        #print(f'[>] Client {ca} sent comm:det {packet.comm}:{packet.det}')


        #print()
        if packet.comm[0] == '/':


            if packet.comm == '/answer':

                print(f'[>] Client {ca} sent answer: {packet.det}')

                self.question_queue.append([ca, packet.det])
                self.question_queue_change = True

            elif packet.comm == '/name':

                print(f'[>] Client {ca} has set their name as: {packet.det}')
                self.names[cs] = packet.det

            else:
                pass

    def client_disconnected(self, cs, e):

        """Cleanly exits a connection with a client,
           with an optional exception."""

        print()
        print(f'[!] Client {self.client_addr[cs]} disconnected: {e}')

        self.client_sockets.remove(cs)
        del self.client_addr[cs]

        cs.close()


    def listen_for_client(self, cs):

        """Listens for a singular cluient as thread t."""

        while True:

            try:

                msg = cs.recv(1024).decode()
                msg = msg.split(self.st)

                pk = Packet(msg[0], msg[1])

                #print(pk)

            except BaseException as e:

                self.client_disconnected(cs, e)
                break

            else:

                self.intr_command(cs, pk)


    def loop(self):

        """Loops the program. Can change state
           to do different tasks."""

        print()

        while True:

            if self.state == 'Lobby':

                try:
                    client_socket, client_address = self.s.accept()
                    print()
                    print(f'[+] New Client Connected: {client_address}')

                    self.client_sockets.add(client_socket)
                    self.client_addr[client_socket] = client_address

                    t = Thread(target = self.listen_for_client, args = (client_socket,),
                               daemon = True)
                    t.start()

                except:
                    pass

            elif self.state == 'Game':
                pass

            elif self.state == 'After Game':
                pass

            else:
                pass

        self.exit()


    def return_cs(self, ca):

        """Return a socket when given a address."""

        try:
            saddr = {value:key for key, value in self.client_addr.items()}
            return saddr[ca]

        except:
            return False

