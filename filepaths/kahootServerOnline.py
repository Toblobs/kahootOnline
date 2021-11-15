### Hosted on Github at @Toblobs
### A Synergy Studios Project

version = '1.0.3'

from netlib import Server, Client, Packet
from netlib.net.server.connection import Connection

#==============================================================#


class Question:
    """A singular representation of a question
       in the program. Can edit itself and is passed to
       json in the save."""

    def __init__(self, question, correct):
        self.question = question
        self.correct = correct

    def check_correct(self, resp):

        pass

        ### Example of (abstract?) class method
    

class SimpleAnswerQuestion(Question):
    """A question that has a simple question and answer.
       Inherits from class <Question>"""

    def __init__(self, question, correct):

        super().__init__(question, correct)

    def check_correct(self, resp):

        super().check_correct(resp)

class MultipleAnswerQuestion(Question):
    """A question that is multiple-answerable.
       Between 2 to 4 choices are allowed. Only one is correct.
       Inherits from class <Question>"""

    def __init__(self, question, correct, answers):

        super().__init__(question, correct)
        
        self.answer1 = answers[0]
        self.answer2 = answers[1]

        if len(answers) >= 3:
            self.answer3 = answers[2]
            
        if len(answers) >= 4:
            self.answer4 = answers[3]

    def check_correct(self, resp):

        super().check_correct(resp)

        
            

class TrueOrFalseQuestion(Question):
    """This question is always true or false.
       Inherits from class <Question>"""

    pass

#==============================================================#

class QuestionMaker:
    """Class which makes questions. It then returns all the questions made
       in that session, and resets itself."""

    pass

class MetaServer:
    """Original Signal Server"""

    PORT = 7777

    def setup_server(h: Server):
        usernames = {}

        @h.OnConnect
        def handle_connection(conn: Connection):

            @conn.OnSignalOfType("set-username")
            def set_username(packet: Packet):
                username = packet.body["username"]
                usernames[conn.UUID] = username

            @conn.OnSignalOfType("send-message")
            def handle_messages(packet: Packet):
                content = packet.body["content"]
                username = usernames[conn.UUID]

                message = Packet({
                    "content": content,
                    "username": username
                }, request_type="message")

                h.send_to_all_except(message, conn)

            @conn.OnDisconnect
            def handle_disconnect():
                username = usernames[conn.UUID]

                h.send_to_all_except(Packet({
                    "username": username
                }, request_type="disconnect-message"))

class KahootServer:
    """The server, which creates Question objects and
       broadcasts info to clients. Uses #signal."""

    def __init__(self):

        self.QuestionMaker = QuestionMaker()
        #self.meta = MetaServer()
    


def test_drive_method():
    pass
test_drive_method()
