import opentdb

class OpenTdbClient(object):
    def __init__(self):
        self.opentdb_session = opentdb.Client()
        self.opentdb_session.getToken()


    def get_categories(self):
        return self.opentdb_session.getCategories()

    def get_questions(self, amount, category_id):
        questions = self.opentdb_session.getQuestions(amount=amount, use_token=True, category=category_id)
        return questions