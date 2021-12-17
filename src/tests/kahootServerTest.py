### Hosted on Github at @Toblobs
### A Synergy Studios Project

version = 'T.0.3'

from threading import Thread
import socket
from time import sleep

from kModules.kQuestions import *
from kModules.printer import *

class KahootGame:
    
    """A representation of a single Kahoot Game."""

    def __init__(self):

        self.server = SocketServer()
        self.name = 'eu.kahoot.test.1'

        self.st = '%'
        self.t = Thread(target = self.server.start_server, daemon = True)

        self.QATIME = 10
        self.questions = []
        self.leaderboard = []

        self.printer = Printer()

    def load_questions(self):

        """Loads in questions for the game."""

        # Example code (will be replaced)

        question1 = SimpleAnswerQuestion('What is the second-biggest continent?',  'Africa')
        question2 = MultipleAnswerQuestion('How many degrees does a right angle have?',
                                           '90', ['65', '85', '90', '105'])

        self.questions.append(question1)
        self.questions.append(question2)

    def run_question(self, q):

        """Prints out an appropriate question and
           sends it to clients."""

        if isinstance(q, SimpleAnswerQuestion):
            
            print(f'[?] Question {self.questions.index(q) + 1}: {q.question} | Answer: {q.correct}')
            self.server.broadcast('all', f'/question{self.st}{q.question}')
                
        elif isinstance(q, MultipleAnswerQuestion):
            
            print(f'[?] Question {self.questions.index(q) + 1}: {q.question} | Choices: {q.answers} | Answer: {q.correct}')

            con_answers = ''
            
            for _q in q.answers:

                if con_answers != '':
                    con_answers = con_answers + ', ' + _q
                else:
                    con_answers = con_answers + _q
                    
            self.server.broadcast('all', f'/question{self.st}{q.question};{con_answers}' )          
        
    def start_game(self):

        """Starts and runs a game."""

        self.printer.print_border('double-space')
        print('Starting a new game...')
        self.printer.print_border('single-border')

        self.server.broadcast('all', f'/gamestart{self.st}{self.name}')
        self.server.state = 'Game'

        #Main Game running loop
        for q in self.questions:

            self.server.question_queue = []

            print()

            self.run_question(q)                
            print(f'[>] Question sent to clients!')
            print()

            time_left = self.QATIME
            time_board = []
            old_length = len(self.server.question_queue)

            while time_left >= 0:

                new_length = len(self.server.question_queue)
                
                if old_length < new_length:
                    
                    new_answer = self.server.question_queue[-1:]
                    
                    time_taken = round((self.QATIME - time_left), 2)
                    time_board.append(time_taken)

                old_length = new_length
                sleep(0.01)
                time_left = time_left - 0.01

            print()
            print(f'Client response times: {time_board}')
            print(f'Client answers: {self.server.question_queue}')

            for s in self.server.question_queue:
                #Assign points to leaderboard
                pass


        self.end_game()
            

    def lobby(self):

        """The lobby. When one of the conditions is fufilled,
           exits the while loop and starts the game."""

        self.server.state = 'Lobby'

        print('Waiting lobby time...')
        self.printer.print_border('single-border')

        counter = 15
        list_length = len(self.server.client_sockets)
        
        while True:
            
            if len(self.server.client_sockets) >= (self.server.max_users - 5):
                break
                
            elif counter == 0:
                break

            elif (counter == 10) or (counter == 5) or (counter == 3):
                print(f'Starting in {counter} seconds...')

            if list_length != len(self.server.client_sockets):
                counter = 10
                list_length = len(self.server.client_sockets)
                print('[!] Lobby Timer reset as someone left/joined!')
                print()

            counter = counter - 1
            sleep(1)

        self.start_game()
        
    def run(self):

        """The main running of the KahootGame class."""

        print('Booting...')
        self.printer.print_border('double-border')

        # Boot

        sleep(0.1)
        self.load_questions()

        sleep(0.1)
        self.t.start()

        # Lobby
        
        sleep(0.1)
        self.lobby()

    def end_game(self):

        """Ends the game."""

        # Endgame stuff (wil be coded later)
        self.server.state = 'After Game'
        
        self.printer.print_border('double-border')
        print('[!] Game ended!')
        print()
        print('[*] Points leaderboard:')

        self.server.broadcast('all', 'f/gameover{self.st}{self.name}')

        self.printer.print_border('single-border')
        print()
        print('[!] Shutting down server...')
        self.server.exit_server()
        
        print('[*] Closing application...')
        quit()


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
        self.question_queue = []

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

    def broadcast(self, to, data):

        """Broadcasts the data to every client in our list,"""

        if to == 'all':
            
            for cs in self.client_sockets:
                cs.send(data.encode(self.format))

    def intr_command(self, cs, ca, msg):

        """Handldes commands from the message defined
           and prints out the various info."""

        msg_list = msg.split(self.st)

        comm = msg_list[0]
        det = msg_list[1]

        #print()
        #print(f'[>] Client {ca} sent comm:det {comm}:{det}')

        if comm[0] == '/':

            if comm == '/confo':
                #print(f'[>] Client {ca} confirmation message received!')
                #self.send(cs, f'/confo{self.st}confo_received')
                pass

            elif comm == '/answer':
                print(f'[>] Client {ca} sent answer: {det}')
                self.question_queue.append([ca, det])

            else:
                pass

    def client_disconnected(self, cs, ca, e):

        """Cleanly exits a connection with a client,
           with an optional exception."""

        print()
        print(f'[!] Client {ca} disconnected: {e}')
        self.client_sockets.remove(cs)
        cs.close()

        
    def listen_for_client(self, cs, ca):

        """Listens for a singular cluient as thread t."""

        while True:

            try:

                msg = cs.recv(1024).decode()

            except BaseException as e:
                
                self.client_disconnected(cs, ca, e)
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

            elif self.state == 'Game':
                pass

            elif self.state == 'After Game':
                pass

            else:
                pass

        self.exit()

    
#-------------------------------------------------------------------#

k = KahootGame()
k.run()
