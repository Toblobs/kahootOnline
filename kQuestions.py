from uuid import uuid4

version = '1.0.1'

class Question:
    """A singular representation of a question
       in the program. Can edit itself and is passed to
       json in the save."""

    def __init__(self, question, correct):
        self.question = question
        self.correct = correct

        self.uuid = uuid4()

    def check_correct(self, resp):

        pass

        ### Example of (abstract?)
    

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

    def __init__(self, question, correct, answers):

        super().__init__(question, correct)

    def check_correct(self, resp):

        super().check_correct(resp)


class QuestionMaker:
    """Class which makes questions. It then returns all the questions made
       in that session, and resets itself."""

    pass
