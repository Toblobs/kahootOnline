### Hosted on Github at @Toblobs
### A Synergy Studios Project

version = 'T.0.3'

from threading import Thread
import socket

class SocketClient:
    
    """The client, which accepts questions and
       answers them by sending back socket data."""


    def __init__(self):

        self.SERVER_HOST = '127.0.0.1'
        self.SERVER_PORT = 7979

        self.MY_IP = socket.gethostbyname(socket.gethostname())

        self.st = '%'
        self.s = socket.socket()

        self.format = 'UTF-8'

        self.game_running = False

    def start(self):

        """Starts the connection to the host."""

        try:

            print(f'[*] <Client> attempting to connect to {self.SERVER_HOST}:{self.SERVER_PORT}...')
            self.s.connect((self.SERVER_HOST, self.SERVER_PORT))
            print(f'[+] Connection succesful to {self.SERVER_HOST}:{self.SERVER_PORT}!')

        except BaseException as e:
            self.exit(e)

        self.loop()

    def exit(self, error = None):

        """Exits the connection with an optional error."""

        print()
        self.s.close()
        print(f'[!] <Client> shutdown with error: {error}')

    def send(self, data):

        """Sends data to the server, encoded in the specified format."""
        
        self.s.send(data.encode(self.format))

    def get_answer(self, det):

        if ';' not in det:
            answer = input(f'[?] Text Question: {det}: ')

        else:

            question = det.split(';')[0]
            choices = det.split(';')[1]
            
            answer = input(f'[?] Choice Question: {question} | Choices: {choices}: ')
            
        if answer:
            self.send(f'/answer{self.st}{answer}')
        
    def intr_command(self, msg):

        """Examines a command from the server and acts on it."""
        
        msg_list = msg.split(self.st)

        comm = msg_list[0]
        det = msg_list[1]

        print()
        #print(f'[>] Recieved from <Server> object comm:det {comm}:{det}')

        if comm[0] == '/':

            if comm == '/gamestart':
                self.game_running = True
                print(f'[!] Kahoot Game from {det} about to start!')

            elif comm == '/question':
                self.get_answer(det)
                
            elif comm == '/gameover':
                self.end_game()
    

    def listen_for_messages(self):

        """Threaded listening for messages from the host/server."""

        while True:

            try:

                msg = self.s.recv(1024).decode(self.format)
                
            except BaseException as e:

                self.exit(e)
                break

            else:

                self.intr_command(msg)     
        

    def loop(self):

        """The main loop."""

        print()

        t = Thread(target = self.listen_for_messages)
        t.daemon = True #Ends when main thread ends
        t.start()

        self.send(f'/confo{self.st}new_client')
        #print(f'[>] Sent confirmation message to <Server> object')

        while True:

            if self.game_running:
                pass

            else:
                pass

    def end_game(self):

        """Ends the game and shows useful data."""

        self.game_running = False
        print(f'[!] Kahoot Game from {det} finished!')
        self.exit()


#-------------------------------------------------------------------#

g = SocketClient()
g.start()

