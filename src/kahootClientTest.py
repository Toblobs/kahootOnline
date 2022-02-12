### Hosted on Github at @Toblobs
### A Synergy Studios Project

version = 'T.0.5.1'

from threading import Thread
from time import sleep
from datetime import datetime

import socket

from kModules.printer import *

#from kModules.net.client import SocketClient
from kModules.net.packet import Packet
        
class SocketClient:

    """The client, which accepts questions and
       answers them by sending back socket data."""


    def __init__(self):

        self.printer = Printer()

        self.SERVER_HOST = '127.0.0.1'
        self.SERVER_PORT = 7979

        self.MY_IP = socket.gethostbyname(socket.gethostname())

        self.st = '%'
        self.s = socket.socket()

        self.format = 'UTF-8'

        self.game_running = False

        self.answered_question = False

    def start_client(self):

        """Starts the connection to the host."""

        print('Booting Client...')
        self.printer.print_border('double-border')

        name = input('Please input a name: ')
        
        while name == '':
            name = input('Please input a name: ')

        print()

        self.SERVER_HOST = input('Please enter an IP: ')

        while name == '':
            self.SERVER_HOST = input('Please enter an IP: ')

            
        self.printer.print_border('single-border')
        print()
        
        try:

            print(f'[*] <Client> attempting to connect to {self.SERVER_HOST}:{self.SERVER_PORT}...')
            self.s.connect((self.SERVER_HOST, self.SERVER_PORT))
            print(f'[+] Connection succesful to {self.SERVER_HOST}:{self.SERVER_PORT}!')

        except BaseException as e:
            self.exit(e)

        self.send(Packet('/name', f'{name}'))

        self.loop()

    def exit(self, error = None):

        """Exits the connection with an optional error."""

        print()
        self.s.close()
        print(f'[!] <Client> shutdown with error: {error}')
        quit()

    def send(self, packet):

        """Sends data to the server, encoded in the specified format."""

        self.s.send(packet.unwrap(self.st).encode(self.format))

    def get_answer(self, comm, det):

        self.printer.print_border('double-border')

        if comm == '/SAQquestion':

            answer = input(f'[?] Text Question: {det}: ')

            #while (';' in answer) or ('/' in answer):
                #print('Invalid input! You cannot use special characters ; or /')
                #answer = input(f'[?] Text Question: {quesexecutingtion} | Choices: {choices}: ')

        elif comm == '/MAQquestion':

            question = det.split(';')[0]
            choices = det.split(';')[1]

            answer = input(f'[?] Choice Question: {question} | Choices: {choices}: ')

            #while (';' in answer) or ('/' in answer):
                #print('Invalid input! You cannot use special characters ; or /')
                #answer = input(f'[?] Choice Question: {question} | Choices: {choices}: ')

        elif comm == '/TOFQquestion':

            answer = input(f'[?] True Or False Question: {det}: ')

            #while (';' in answer) or ('/' in answer):
                #print('Invalid input! You cannot use special characters ; or /')
                #answer = input(f'[?] Text Question: {question} | Choices: {choices}: ')


        self.send(Packet('/answer', f'{answer}'))
        self.answered_question = True
        
        self.printer.print_border('single-border')
        

    def print_lb_info(self, det):

        """Prints out the position of the player."""

        position = det.split(';')[0]
        points = det.split(';')[1]

        print(f'[>] You are in position {position}, with {points} points.')

        self.printer.print_border('single-border')
        print()
        

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

            elif comm in ['/SAQquestion', '/MAQquestion', '/TOFQquestion']:
                self.answered_question = False
                self.get_answer(comm, det)

            elif comm == '/gameover':
                self.end_game(det)

            elif comm == '/lb_info':
                self.print_lb_info(det)

            elif comm == '/correct':
                print(f'[?] You got the question {det}!')

            elif comm == '/got_points':
                print(f'[!] You got {det} points!')
                
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

        while True:

            if self.game_running:
                pass

            else:
                pass

    def end_game(self, det):

        """Ends the game and shows useful data."""

        self.game_running = False
        print(f'[!] Kahoot Game from {det} finished!')
        self.exit()


#-------------------------------------------------------------------#

g = SocketClient()
g.start_client()
