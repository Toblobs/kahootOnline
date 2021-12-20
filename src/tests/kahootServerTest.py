### Hosted on Github at @Toblobs
### A Synergy Studios Project

version = 'T.0.4'
#NOTE: DPN'T FORGET TO UPDATE kModules on GitHub

from threading import Thread
import socket
from time import sleep

from kModules.kQuestions import *
from kModules.printer import *

class KahootGame:
    
    """A representation of a single Kahoot Game."""

    def __init__(self):

        self.server = SocketServer()
        self.printer = Printer()
        self.name = 'eu.kahoot.test.1'

        self.st = '%'
        self.t = Thread(target = self.server.start_server, daemon = True)

        self.qa_time = 10
        
        self.leaderboard = {}

        self.max_points = 1000

        self.questions = []
        self.question_pack = [starterPack1, 'all']

        self.lobby_wait = 10

    def load_questions(self):

        """Loads in questions for the game."""

        if self.question_pack != None:

            if self.question_pack[1] == 'all':
                self.question_pack[0].add_pack(self.questions)

            else:
                pass


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
                    
            self.server.broadcast('all', f'/question{self.st}{q.question};{con_answers}')
            
    def print_leaderboard(self, q = None):

        """Prints out the leaderboard."""

        print()

        if q:
            print(f'Leaderboard as of Question {self.questions.index(q) + 1}:')


        swapped_dict = {value:key for key, value in self.leaderboard.items()}
        sdl = list(swapped_dict.items())

        sdl.sort(reverse = True)

        print(sdl)
                
        for s in sdl:

            SUFFIXES = {1: 'st', 2: 'nd', 3: 'rd'}

            if 10 <= ((sdl.index(s) + 1) % 100) <= 20:
                suffix = 'th'

            else:
                suffix = SUFFIXES.get((sdl.index(s) + 1) % 10, 'th')

            pos_string = str(sdl.index(s) + 1) + suffix
  
            print(f'{pos_string}: {s[1]} | Points: {s[0]}')


    def assign_points(self, s, q, time_taken):
        
        """Assigns points to each client."""

        correct = (q.correct == s[1])
        print(f'[+] Client {s[0]} got the question {correct}!')

        if correct:
                
            #Assign points to each correct answer
            
            val = time_taken / self.qa_time
            val = 1 - (val / 2)

            s_points = round(self.max_points * val)

        else:

            #Add 0 points to that client
            s_points = 0

        #print(f'[+] Client {s} got {s_points} points!')

        if s[0] in self.leaderboard:
            self.leaderboard[s[0]] = self.leaderboard[s[0]] + s_points

        else:
            self.leaderboard[s[0]] = s_points 
        
    def run_game(self):

        """Starts and runs a game."""

        print()
        print('Starting a new game...')
        self.printer.print_border('double-border')

        self.server.broadcast('all', f'/gamestart{self.st}{self.name}')
        self.server.state = 'Game'

        #Main Game running loop
        for q in self.questions:

            if len(self.server.client_sockets) > 0:

                self.server.question_queue = []

                print()

                self.run_question(q)                
                print(f'[>] Question sent to clients!')
                print()

                time_left = self.qa_time
                time_board = []

                while time_left >= 0:
                    
                    if self.server.question_queue_change:

                        new_answer = self.server.question_queue[-1:]
                        
                        time_taken = round((self.qa_time - time_left), 2)
                        time_board.append(time_taken)

                        self.server.question_queue_change = False

                    if len(self.server.question_queue) >= len(self.server.client_sockets):
                        break

                    sleep(0.1)
                    time_left = time_left - 0.1


                print()
                #print(f'Client response times: {time_board}')
                print(f'Client answers: {self.server.question_queue}')

                for s in self.server.question_queue:
                    self.assign_points(s, q, time_board[self.server.question_queue.index(s)])

                if self.questions.index(q) != len(self.questions) - 1:
                    self.print_leaderboard(q)

                print()
                self.printer.print_border('single-border')
            
        self.end_game()
            

    def lobby(self):

        """The lobby. When one of the conditions is fufilled,
           exits the while loop and starts the game."""

        self.server.state = 'Lobby'

        print('Waiting lobby time...')
        self.printer.print_border('single-border')

        counter = self.lobby_wait
        list_length = len(self.server.client_sockets)
        
        while True:
            
            if len(self.server.client_sockets) >= (self.server.max_users - 5):
                break
                
            elif counter == 0:
                break

            elif (counter == 10) or (counter == 5) or (counter == 3):
                print(f'Starting in {counter} seconds...')

            if list_length != len(self.server.client_sockets):
                counter = self.lobby_wait
                list_length = len(self.server.client_sockets)
                print('[!] Lobby Timer reset as someone left/joined!')
                print()

            counter = counter - 1
            sleep(1)

        self.run_game()
        
    def start(self):

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
        self.server.broadcast('all', f'/gameover{self.st}{self.name}')
        print('[!] Game ended!')

        print()
        print('[*] Final Points leaderboard:')
        self.print_leaderboard()

        print()
        self.printer.print_border('double-border')
        print()
        
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
                self.question_queue_change = True

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

                try:
                    client_socket, client_address = self.s.accept()
                    print(f'[+] New Client Connected: {client_address}')

                    self.client_sockets.add(client_socket)

                    t = Thread(target = self.listen_for_client, args = (client_socket, client_address),
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

    
#-------------------------------------------------------------------#

k = KahootGame()
k.start()
