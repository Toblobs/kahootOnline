import csv

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

    def check_correct(self, resp):

        return resp.lower() == self.correct.lower()
    

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

        assert correct in answers, "MultipleAnswerQuestion() must have a correct answer in its list of answers!"
        assert len(answers) >= 2, "MultipleAnswerQuestion() must have a list of at least 2 answers!"

        self.answers = answers
        
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

    def __init__(self, question, correct):

        super().__init__(question, correct)

        assert correct in ['True', 'False'], "TrueOrFalseQuestion() must have a correct answer of True or False!"

    def check_correct(self, resp):

        super().check_correct(resp)
        
#------------------------------------------------------------------------------#


# Starter Pack 1 (3 questions)

sp1_1 = SimpleAnswerQuestion('What is the second biggest continent?', 'Africa')
sp1_2 = MultipleAnswerQuestion('How many degrees does a right angle have?', '90', ['65', '70', '90', '105'])
sp1_3 = SimpleAnswerQuestion('How many sides does a heptagon have?', '7')
sp1_4 = SimpleAnswerQuestion('Who won the 2016 World Cup?', 'France')
sp1_5 = MultipleAnswerQuestion('How many plays did Shakespeare write?', '37', ['28', '37', '42', '50'])

starterPack1 = Pack('Starter Pack 1', [sp1_1, sp1_2, sp1_3, sp1_4, sp1_5])


# Starter Pack 2

sp2_1 = SimpleAnswerQuestion('How long is an Olympic swimming pool in meters?', '50')
sp2_2 = MultipleAnswerQuestion('What shape is used for a tradional red stop sign?', 'Octagon', ['Triangle', 'Octagon', 'Square', 'Penatgon'])
sp2_3 = TrueOrFalseQuestion('The Artic is the largest ocean on earth.', 'False')
sp2_4 = MultipleAnswerQuestion('Who was the first president of the United States?', 'George Washington', ['George Washington', 'Barack Obama', 'Donald Trump'])
sp2_5 = TrueOrFalseQuestion('Area 51 is located in Nevada.', 'True')
sp2_6 = SimpleAnswerQuestion('Which country has the most natural lakes?', 'Canada')
sp2_7 = MultipleAnswerQuestion('How long do elephant pregnancies last?', '22', ['22', '25', '28',])
sp2_8 = MultipleAnswerQuestion('What is the (average) temperature of Venus in degrees?', '460', ['380', '627', '343', '460'])
sp2_9 = TrueOrFalseQuestion('William Shakespeare invented the word "vomit".', "True")
sp2_10 = SimpleAnswerQuestion("How long is New Zealand's Ninety Mile Beach? (in miles)?", "55")

starterPack2 = Pack('Starter Pack 2', [sp2_1, sp2_2, sp2_3, sp2_4, sp2_5, sp2_6, sp2_7, sp2_8, sp2_9, sp2_10])

