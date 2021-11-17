### Hosted on Github at @Toblobs
### A Synergy Studios Project

version = '1.0.5'

from netlib import Server, Signal
from netlib.net.server.connection import Connection
from uuid import uuid4

from kQuestions import *

class KahootServer:
    """The server, which creates Question objects and
       broadcasts info to clients. Uses #signal."""

    def __init__(self):

        self.QuestionMaker = QuestionMaker()

        self.ip = Server.get_host_machine()
        self.port = 9999
        
        self._server = Server(self.ip, self.port)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self._server.exit()
    
    def run(self):
        self._server.run()

    def stop(self):
        self._server.exit()


correct = 'B'

with KahootServer() as ks:
    
    @ks._server.OnConnection
    def handle_connection(conn):
        
        @conn.OnSignal("is_answer_correct")
        def is_correct(signal):
            correct = (signal.payload.answer == correct_answer) #Make correct

            conn.send(Signal({"correct": correct, "id": question_id}, "answer_status")) 
