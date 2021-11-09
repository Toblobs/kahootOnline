# Hosted on Github at @Toblobs
# A Synergy Studios Project


class Question:
    """A singular representation of a question
       in the program. Can edit itself and is passed to
       json in the save."""

    def __init__(self, question, correct):
        self.question = question
        self.correct = correct
    

class SimpleAnswerQuestion(Question):
    pass

class MultipleAnswerQuestion(Question):
    """A question that is multiple-answered.
       Between 2 to 4 choices. Only one is correct."""

    def __init__(self, noq, answer1, answer2, answer3, answer4,):

        super().__init__(self, question, correct)
        
        self.answer1 = answer1
        self.answer2 = answer2

        self.noq = noq
        
        if self.noq == 2:
            pass
        
        elif self.noq == 3:
            self.answer3 = answer3
            
        elif self.noq == 4:
            self.answer3 = answer3
            self.answer4 = answer4
            
    def check_correct(self, no):
        pass

class TrueOrFalseQuestion(Question):
    pass




class KahootServer():
    """Handling of sockets."""

    def __init__(self):
        pass
    



