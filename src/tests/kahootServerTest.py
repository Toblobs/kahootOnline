### Hosted on Github at @Toblobs
### A Synergy Studios Project

version = 'T.0.5.1'

from threading import Thread
from time import sleep

from kModules.kQuestions import *
from kModules.printer import Printer

from kModules.net.socket_server import SocketServer
from kModules.net.packet import Packet


class InputReader:

    """Reads input from the user for commands."""

    def __init__(self):

        self.commands = []
        self.command_queue = []

    def start(self):

        while True:

            read = input()
            self.intr_command(read)

class Leaderboard:

    """Represents the leaderboard in the game."""

    def __init__(self):
        
        self.leaderboard = []

    def refresh_leaderboard(self):

        """Reorders and updates the leaderboard."""
        
        self.leaderboard = sorted(self.leaderboard, key = lambda tup: tup[1], reverse = True)
        
    def append(self, key, value, autosort = False):

        """Add a value to the leaderboard.
           If autosort is True, refreshes the leaderboard"""

        self.leaderboard.append((key, value))

        if autosort:
            self.refresh_leaderboard()

    def add_points(self, key, value, autosort = False):

        """Adds points to a key in the leaderboard.
           If autosort is True, refreshes the leaderboard"""

        if self.return_position(key):

            old_value = self.return_points(key)
            new_value = old_value + value
            
            self.leaderboard[self.return_position(key)] = (key, new_value)

    def print_leaderboard(self, q = None):

        """Prints out the leaderboard."""

        print()

        if q:
            
            print(f'Leaderboard as of Question {q}:')

        for s in self.leaderboard:

            print(f'{self.leaderboard.index(s) + 1}: {s[0]} | Points: {s[1]}')

    def return_position(self, name):

        """Returns a position based on the key (name)"""

        for s in self.leaderboard:

            if s[0] == name:
                return self.leaderboard.index(s)

    def return_points(self, name):

        """Returns a position based on the name."""

        for s in self.leaderboard:

            if s[0] == name:
                return s[1]
            

class KahootGame:

    """A representation of a single Kahoot Game."""

    def __init__(self):

        self.server = SocketServer()
        self.leaderboard = Leaderboard()
        
        self.printer = Printer()
        self.input_reader = InputReader()

        self.name = 'eu.kahoot.test.1'
        self.st = self.server.st

        self.t = Thread(target = self.server.start_server, daemon = True)
        #self.t1 = Thread(targer = self.input_reader.start, daemon = True)

        self.qa_time = 20

        self.max_points = 1000

        self.questions = []
        self.question_pack = [starterPack2, 'all']

        self.lobby_wait = 20

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

            print(f'[?] Text Question {self.questions.index(q) + 1}: {q.question} | Answer: {q.correct}')
            self.server.broadcast('all', Packet('/SAQquestion', f'{q.question}'))

        elif isinstance(q, MultipleAnswerQuestion):

            print(f'[?] Choice Question {self.questions.index(q) + 1}: {q.question} | Choices: {q.answers} | Answer: {q.correct}')

            con_answers = ''

            for _q in q.answers:

                if con_answers != '':
                    con_answers = con_answers + ', ' + _q
                else:
                    con_answers = con_answers + _q

            self.server.broadcast('all', Packet('/MAQquestion', f'{q.question};{con_answers}'))

        elif isinstance(q, TrueOrFalseQuestion):

            print(f'[?] True/False Question {self.questions.index(q) + 1}: {q.question} | Answer: {q.correct}')
            self.server.broadcast('all', Packet('/TOFQquestion', f'{q.question}'))


    def assign_points(self, s, q, time_taken):

        """Assigns points to each client."""

        addr = s[0]
        name = self.server.names[self.server.return_cs(addr)]
        
        correct = (q.correct == s[1])
        
        if correct == True:
            correct = 'correct'
            
        else:
            correct = 'wrong'
            
        print(f'[-] Client {name} got the question {correct}!')

        if correct ==  'correct':

            #Assign points to each correct answer

            val = time_taken / self.qa_time
            val = 1 - (val / 2)

            s_points = round(self.max_points * val)

        else:

            #Add 0 points to that client
            s_points = 0

        #print(f'[+] Client {addr} got {s_points} points!')
        self.server.send(self.server.return_cs(addr), Packet('/got_points', f'{s_points}'))

        if self.leaderboard.return_position(name) == None:
            self.leaderboard.append(name, s_points)

        else:
            self.leaderboard.add_points(name, s_points)
            

        self.server.send(self.server.return_cs(addr), Packet('/correct', f'{correct}'))

        position = self.leaderboard.return_position(name) + 1
        points = self.leaderboard.return_points(name)

        sleep(0.2)

        self.server.send(self.server.return_cs(addr), Packet('/lb_info', f'{position};{points}'))

    def run_game(self):

        """Starts and runs a game."""

        print()
        print('Starting a new game...')
        self.printer.print_border('double-border')

        self.server.broadcast('all', Packet('/gamestart', f'{self.name}'))
        self.server.state = 'Game'

        #Main Game running loop
        for q in self.questions:

            if len(self.server.client_sockets) > 0:

                self.server.question_queue = []

                print()

                self.run_question(q)
                #print(f'[>] Question sent to clients!')
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
                    self.leaderboard.refresh_leaderboard()
                    self.leaderboard.print_leaderboard(self.questions.index(q) + 1)

                print()
                self.printer.print_border('single-border')

            else:

                self.end_game()

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
                print('[!] Lobby Timer interrupted as someone left/joined!')
                print()

                counter += 5
                list_length = len(self.server.client_sockets)

            counter = counter - 1
            sleep(1)

        self.run_game()

    def start(self):

        """The main running of the KahootGame class."""

        print('Booting Server...')
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
        self.server.broadcast('all', Packet('/gameover', f'{self.name}'))
        print('[!] Game ended!')

        print()
        print('[*] Final Points leaderboard:')
        self.leaderboard.print_leaderboard()

        print()
        self.printer.print_border('double-border')
        print()

        print('[*] Closing application...')
        quit()

#-------------------------------------------------------------------#

k = KahootGame()
k.start()
