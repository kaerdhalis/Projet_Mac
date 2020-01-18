class Question(object):
    def __init__(self, question, answer, wrong_answers, category):
        self.question = question
        self.answer = answer
        self.wrong_answers = wrong_answers
        self.category = category
