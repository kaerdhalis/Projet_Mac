from pyArango.connection import *
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
        if not self.db.hasCollection("games"):
            self.games_collection = self.db.createCollection(name="games")

    def add_player(self, telegram_id, name):
        new_player = self.players_collection.createDocument()
        new_player["name"] = name
        new_player._key = telegram_id
        new_player.save()

    def get_player(self, telegram_id):
        return self.players_collection[telegram_id]


    def add_new_game(self, chat_id):
        new_game= self.games_collection.createDocument()
