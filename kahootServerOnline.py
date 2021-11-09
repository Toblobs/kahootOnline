### Hosted on Github at @Toblobs
### A Synergy Studios Project

version = '1.0.2'

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
    pass


class KahootServer():
    """The server, which creates Question objects and
       broadcasts info to clients. Uses #signal."""

    def __init__(self):
        pass


def test_drive_method():
    
    maq = MultipleAnswerQuestion('Test Question?', 2, ['a', 'b', 'c'])
    maq.check_correct('b') 

test_drive_method()
