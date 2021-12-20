from uuid import uuid4

version = '1.0.3'

class Pack():

    """Holds lots of questions in one list."""

    def __init__(self, title, questions):
        
        self.title = title
        self.questions = questions

    def add_pack(self, to_add):

        for q in self.questions:
            to_add.append(q)
            
class Question:
    
    """A singular representation of a question
       in the program. Can edit itself and is passed to
       json in the save."""

    def __init__(self, question, correct):
        
        self.question = question
        self.correct = correct

        self.uuid = uuid4()

    def check_correct(self, resp):

        return resp == self.correct
    

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

        self.answers = answers
        
        self.answer1 = answers[0]
        self.answer2 = answers[1]

        if len(answers) >= 3:
            self.answer3 = answers[2]
            
        if len(answers) >= 4:
            self.answer4 = answers[3]

    def check_correct(self, resp):

        super().check_correct(resp)

        
    
class TrueOrFalseQuestion():
    
    """This question is always true or false.
       Inherits from class <Question>"""

    pass

#------------------------------------------------------------------------------#


# Starter Pack 1 (3 questions)

sp1_1 = SimpleAnswerQuestion('What is the second biggest continent?', 'Africa')
sp1_2 = MultipleAnswerQuestion('How many degrees does a right angle have?',
                               '90', ['65', '70', '90', '105'])
sp1_3 = SimpleAnswerQuestion('How many sides does a heptagon have?', '7')

starterPack1 = Pack('Starter Pack 1', [sp1_1, sp1_2, sp1_3])
