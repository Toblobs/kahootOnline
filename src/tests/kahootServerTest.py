### Hosted on Github at @Toblobs
### A Synergy Studios Project

version = '1.0.7_T.0.2'

from threading import Thread
import socket
from time import sleep

def print_special(sp = None):

    """Special Printing Class"""

    if sp == None:
        pass

    #Borders
    
    elif sp == 'single-border':
        print('-' * 30)
        
    elif sp == 'double-border':
        print('_' * 30)
        print('-' * 30)
        print()

    elif sp == 'equals-border':
        print('=' * 30)

    #Spaces

    elif sp == 'double-space':
        print()
        print()

    
        
class KahootGame:
    
    """A representation of a single Kahoot Game."""

    def __init__(self):

        self.server = SocketServer()

        self.st = Thread(target = self.server.start_server, daemon = True)

    def start_game(self):

        print_special('double-space')
        print('Starting a new game...')
        print_special('single-border')
        

    def lobby(self):

        """The lobby. When one of the conditions is fufilled,
           exits the while loop and starts the game."""

        self.server.state = 'Lobby'

        print('Waiting lobby time...')
        print_special('single-border')

        counter = 10
        list_length = len(self.server.client_sockets)
        
        while True:
            
            if len(self.server.client_sockets) >= (self.server.max_users - 5):
                self.start_game()
                
            elif counter == 0:
                self.start_game()

            elif (counter == 5) or (counter == 3) or (counter == 1):
                print(f'Starting in {counter} second(s)...')

            if list_length != len(self.server.client_sockets):
                counter = 10
                list_length = len(self.server.client_sockets)
                print('Lobby Timer Reset!')

            counter = counter - 1
            sleep(1)

    def run(self):

        """The main running of the KahootGame class."""

        print('Booting...')
        print_special('double-border')
        
        sleep(3)
        self.st.start()

        sleep(1)
        self.lobby()



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

    def send(self, cs, data):

        """Sends data to the client as encoded in the specified format."""

        cs.send(data.encode(self.format))

    def intr_command(self, cs, ca, msg):

        """Handldes commands from the message defined
           and prints out the various info."""

        msg_list = msg.split(self.st)

        comm = msg_list[0]
        det = msg_list[1]

        print()
        print(f'[>] Client {ca} sent comm:det {comm}:{det}')

        if comm[0] == '/':

            #if comm == '/confo':
                #print(f'[>] Client {ca} confirmation message received!')
                #self.send(cs, f'/confo{self.st}confo_received')

            if comm == '':
                pass

            else:
                pass

        
    def listen_for_client(self, cs, ca):

        """Listens for a singular cluient as thread t."""

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

        """Loops the program. Can change state
           to do different tasks."""

        print()

        while True:

            if self.state == 'Lobby':
                client_socket, client_address = self.s.accept()
                print(f'[+] New Client Connected: {client_address}')

                self.client_sockets.add(client_socket)

                t = Thread(target = self.listen_for_client, args = (client_socket, client_address),
                           daemon = True)
                t.start()

            else:
                pass

        self.exit()

    
#-------------------------------------------------------------------#

k = KahootGame()
k.run()
