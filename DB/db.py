from pyArango.connection import *
from pyArango.collection import Collection, Field
from pyArango.graph import Graph, EdgeDefinition
from Decorator.singleton import Singleton

from DB.graph import *


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

        if not self.db.hasCollection("played"):
            self.player_games_collection = self.db.createCollection(name="played")
        else:
            self.player_games_collection = self.db["played"]

        if not self.db.hasGraph("TriviaGraph"):
            self.graph = self.db.createGraph(name="TriviaGraph")
        else:
            self.graph = self.db.graphs['TriviaGraph']

    def add_category(self, category):
        cat_in_db = self.get_category(category)
        if cat_in_db is None:
            new_category = self.categories_collection.createDocument()
            new_category["name"] = category

            new_category.save()
        return cat_in_db

    def get_category(self, cat):
        aql = "FOR c IN categories FILTER c.name==@cat LIMIT 1 " \
              "RETURN c "
        bind_vars = {'cat': cat}
        query_result = self.db.AQLQuery(aql, rawResults=False, batchSize=1, bindVars=bind_vars)

        if not query_result:
            return None
        else:
            return query_result[0]

    def add_question(self, question):
        question_in_db = self.get_question(question.question)
        if question_in_db is None:
            new_question = self.question_collection.createDocument()
            new_question["question"] = question.question
            new_question["answer"] = question.answer
            new_question["wrong_answers"] = question.wrong_answers

            new_question.save()
            cat = self.add_category(question.category)
            self.graph.link('isOfCategory', new_question, cat, {}, waitForSync=True)
            question_in_db = new_question

        return question_in_db

    def get_question(self, question):
        aql = "FOR q IN questions FILTER q.question==@question LIMIT 1 " \
              "RETURN q "
        bind_vars = {'question': question}
        query_result = self.db.AQLQuery(aql, rawResults=False, batchSize=1, bindVars=bind_vars)

        if not query_result:
            return None
        else:
            return query_result[0]

    def add_player(self, telegram_id, name):
        if str(telegram_id) not in self.players_collection:
            new_player = self.players_collection.createDocument()
            new_player["username"] = name
            new_player._key = str(telegram_id)
            new_player.save()

    def add_player_to_game(self, player, game):
        self.graph.link('played', player, game, {"score": 0})

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

    def start_game(self, game):
        game["status"] = "ingame"
        game.save()

    def end_game(self, game):
        game["status"] = "dead"
        game.save()

    def get_active_game(self, chat_id):
        aql = "FOR c IN games FILTER c.chat_id==@chatid &&(c.status == \"init\" || c.status==\"ingame\") LIMIT 10 " \
              "RETURN c "
        bind_vars = {'chatid': chat_id}
        query_result = self.db.AQLQuery(aql, rawResults=False, batchSize=1, bindVars=bind_vars)

        if not query_result:
            return None
        else:
            return query_result[0]

    def add_question_to_game(self, question, game):

        self.graph.link('contains', game, question, {"correct_answer_count": 0, "wrong_answer_count": 0},
                        waitForSync=True)

    def is_player_in_game(self, player, game):
        aql = "FOR p IN played FILTER p._from==@playerid && p._to==@gameid LIMIT 1" \
              "RETURN p "
        bind_vars = {'playerid': player._id, 'gameid': game._id}
        query_result = self.db.AQLQuery(aql, rawResults=False, batchSize=1, bindVars=bind_vars)

        if not query_result:
            return False
        else:
            return True

    def get_player_game_link(self, player, game):
        aql = "FOR p IN played FILTER p._from==@playerid && p._to==@gameid LIMIT 1" \
              "RETURN p "
        bind_vars = {'playerid': player._id, 'gameid': game._id}
        query_result = self.db.AQLQuery(aql, rawResults=False, batchSize=1, bindVars=bind_vars)

        if not query_result:
            return None
        else:
            return query_result[0]

    def get_players_ingame(self,  game):
        aql = "FOR p IN played FILTER p._to==@gameid LIMIT 50" \
              "RETURN p "
        bind_vars = { 'gameid': game._id}
        query_result = self.db.AQLQuery(aql, rawResults=False, batchSize=1, bindVars=bind_vars)

        return query_result

    def set_expected_answer(self, game, char):
        game["expected_answer"] = char;
        game.save()

    def set_current_question(self, game, question):
        game["current_question"] = question._id;
        game.save()

    def add_answer(self, game, player, answer):
        question_id = game["current_question"]
        question_id = question_id.split('/')[1]
        question = self.question_collection[question_id]
        correct = answer == game["expected_answer"]

        self.graph.link('answered', player, question, {"correct": correct},
                        waitForSync=True)

        game_question_link = self.get_game_question_link(game, question)
        prev_wrong_answer_count = game_question_link["wrong_answer_count"]
        prev_correct_answer_count = game_question_link["correct_answer_count"]

        if correct:
            prev_correct_answer_count += 1
            game_question_link["correct_answer_count"] = prev_correct_answer_count
            player_game_link= self.get_player_game_link(player,game)
            player_game_link["score"]=player_game_link["score"]+1
            player_game_link.save()
        else:
            prev_wrong_answer_count += 1
            game_question_link["wrong_answer_count"]= prev_wrong_answer_count

        game_question_link.save()
        print("hey")

        game_question_link

    def get_game_question_link(self, game, question):
        aql = "FOR c IN contains FILTER c._from==@gameid && c._to==@questionid LIMIT 1" \
              "RETURN c "
        bind_vars = {'questionid': question._id, 'gameid': game._id}
        query_result = self.db.AQLQuery(aql, rawResults=False, batchSize=1, bindVars=bind_vars)

        if not query_result:
            return None
        else:
            return query_result[0]

    def get_answer_current_question(self,game):
        question_id = game["current_question"]
        question_id = question_id.split('/')[1]
        question = self.question_collection[question_id]
        return question.answer