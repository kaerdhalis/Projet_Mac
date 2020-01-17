import random

from telegram.ext import Updater, CommandHandler
from telegram.bot import Bot
from DB.db import DB
from Data.models import Question
from Bot.Constants import *


class TriviaBot(object):
    def __init__(self, token):
        self.token = token
        self.bot = Bot(token)
        self.updater = Updater(token, use_context=True)
        self.db = DB.instance()
        self.dispatcher = self.updater.dispatcher
        self.setup_handlers()

    def start(self):
        self.updater.start_polling()
        self.updater.idle()

    def setup_handlers(self):
        self.dispatcher.add_handler(CommandHandler('newgame', self.new_game, pass_chat_data=True))
        self.dispatcher.add_handler(CommandHandler('join', self.join, pass_chat_data=True))

    def new_game(self, update, context):
        chat_id = update.effective_chat.id

        if not self.db.has_active_game(chat_id):
            self.db.add_new_game(chat_id)
            answer = 'Creating Game:\n' \
                     '/join to join the game\n' \
                     '/start to start the game'
        else:
            answer = 'Game already running'
        self.bot.send_message(chat_id, answer)

        # q = Question(1, "comment", "oui", ["non", "ouais", "p-e"])
        # self.ask_question(chat_id, q)
        # update.message.reply_text(answer)

    def join(self, update, context):
        chat_id = update.effective_chat.id
        user_id = update.message.from_user.id
        user_name = update.message.from_user.username
        if not self.db.has_active_game(chat_id):
            answer = "create a game first with:\n /newgame"
            self.bot.send_message(chat_id, answer)
        else:
            self.db.add_player(user_id, user_name)

    def ask_question(self, chat_id, question):
        answers = question.wrong_answers
        answers.append(question.answer)
        random.shuffle(answers)

        text = 'Question:\n'
        text += question.question + '\n'
        letterAscii = 65
        for answer in answers:
            text += chr(letterAscii) + ')' + answer + '\n'
            letterAscii += 1
        self.bot.send_message(chat_id, text, reply_markup=keyboard_markup())

    def create_game(self, chat_id):
        self.db.add(chat_id)
