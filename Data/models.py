
class Question(object):
    def __init__(self, question_id, question, answer, wrong_answers):
        self.id = question_id
        self.question = question
        self.answer = answer
        self.wrong_answers = wrong_answers

    
