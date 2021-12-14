### Hosted on Github at @Toblobs
### A Synergy Studios Project

version = '1.0.4_T.0.2'

from threading import Thread
import socket

class SocketClient:
    """The client, which accepts questions and
       answers them by sending back socket data."""


    def __init__(self):

        self.SERVER_HOST = '10.130.67.24'
        self.SERVER_PORT = 7979

        self.MY_IP = socket.gethostbyname(socket.gethostname())

        self.st = '%'
        self.s = socket.socket()

        self.format = 'UTF-8'

    def start(self):

        try:

            print(f'[*] <Client> attempting to connect to {self.SERVER_HOST}:{self.SERVER_PORT}...')
            self.s.connect((self.SERVER_HOST, self.SERVER_PORT))
            print(f'[+] Connection succesful to {self.SERVER_HOST}:{self.SERVER_PORT}!')


            
        except BaseException as e:
            self.exit(e)

        self.loop()

    def exit(self, error = None):

        print()
        self.s.close()
        print(f'[*] <Client> shutdown with error: {error}')

    def send(self, data):
        
        self.s.send(data.encode(self.format))

    def intr_command(self, msg):
        
        msg_list = msg.split(self.st)

        comm = msg_list[0]
        det = msg_list[1]

        print()
        print(f'[>] Recieved from <Server> object comm:det {comm}:{det}')

        if comm[0] == '/':

            if comm == '/gamestart':
                print(f'[!] Kahoot Game from {det} about to start!')
    

    def listen_for_messages(self):

        while True:

            try:

                msg = self.s.recv(1024).decode(self.format)
                
            except BaseException as e:

                self.exit(e)
                break

            else:

                self.intr_command(msg)     
        

    def loop(self):

        print()

        t = Thread(target = self.listen_for_messages)
        t.daemon = True #Ends when main thread ends
        t.start()

        self.send(f'/confo{self.st}new_client')
        print(f'[>] Sent confirmation message to <Server> object')

        while True:

            #Kahoot Game Code
            pass


#-------------------------------------------------------------------#

g = SocketClient()
g.start()

