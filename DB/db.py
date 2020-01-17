from pyArango.connection import *
from pyArango.collection import Collection, Field
from pyArango.graph import Graph, EdgeDefinition
from Decorator.singleton import Singleton


@Singleton
class DB(object):

    def __init__(self):
        conn = Connection(username="root", password="root")

        if not conn.hasDatabase("triviaDB"):
            self.db = conn.createDatabase(name="triviaDB")
        else:
            self.db = conn["triviaDB"]

        if not self.db.hasCollection("players"):
            self.players_collection = self.db.createCollection(name="players")
        else:
            self.players_collection = self.db["players"]
        if not self.db.hasCollection("categories"):
            self.categories_collection = self.db.createCollection(name="categories")
        else:
            self.categories_collection = self.db["categories"]
        if not self.db.hasCollection("questions"):
            self.question_collection = self.db.createCollection(name="questions")
        else:
            self.question_collection = self.db["questions"]
        if not self.db.hasCollection("games"):
            self.games_collection = self.db.createCollection(name="games")
        else:
            self.games_collection = self.db["games"]

       # if not self.db.hasGraph("TriviaGraph"):
        #    self.graph = self.db.createGraph(name="TriviaGraph")
        #else:
         #   self.graph = self.db.graphs['TriviaGraph']

    def add_category(self, category):
        if category not in self.categories_collection:
            new_category = self.categories_collection.createDocument()
            new_category["name"] = category
            new_category._key = category
            new_category.save()

    def add_question(self, question, correct_answer, wrong_answers):
        new_question = self.question_collection.createDocument()
        new_question["question"] = question
        new_question["answer"] = correct_answer
        new_question["wrong_answers"] = wrong_answers
        new_question.save()

    def add_player(self, telegram_id, name):
        if str(telegram_id) not in self.players_collection:
            new_player = self.players_collection.createDocument()
            new_player["name"] = name
            new_player._key = str(telegram_id)
            new_player.save()

    def get_player(self, telegram_id):
        if str(telegram_id) in self.players_collection:
            return self.players_collection[str(telegram_id)]
        else:
            return None

    def add_new_game(self, chat_id):
        new_game = self.games_collection.createDocument()
        new_game["chat_id"] = chat_id
        new_game["status"] = "init"
        new_game.save()

    def has_active_game(self, chat_id):
        aql = "FOR c IN games FILTER c.chat_id==@chatid &&(c.status == \"init\" || c.status==\"ingame\") LIMIT 10 " \
              "RETURN c "
        bindVars = {'chatid': chat_id}
        queryResult = self.db.AQLQuery(aql, rawResults=False, batchSize=1, bindVars=bindVars)

        if not queryResult:
            return False
        else:
            return True
