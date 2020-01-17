
from telegram.ext import Updater, CommandHandler
from telegram.bot import Bot


class TriviaBot(object):
    def __init__(self, token):
        self.bot = Bot(token)

    def AskQuestion(chat_id, question, self=None):
        self.bot.sendMessagage(chat_id, "test question")
