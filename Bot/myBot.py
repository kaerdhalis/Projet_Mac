import random

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.bot import Bot
from DB.db import DB
from Data.models import Question
from Bot.Constants import *
from DB.opentdbAccess import OpenTdbClient


class TriviaBot(object):
    def __init__(self, token):
        self.token = token
        self.bot = Bot(token)
        self.updater = Updater(token, use_context=True)
        self.opentdb_client = OpenTdbClient()
        self.db = DB.instance()
        self.dispatcher = self.updater.dispatcher
        self.setup_handlers()

    def start(self):
        self.updater.start_polling()
        self.updater.idle()

    def setup_handlers(self):
        self.dispatcher.add_handler(CommandHandler('newgame', self.new_game, pass_chat_data=True))
        self.dispatcher.add_handler(CommandHandler('next', self.next_question, pass_chat_data=True))
        self.dispatcher.add_handler(CommandHandler('start', self.start_game, pass_chat_data=True))
        self.dispatcher.add_handler(CommandHandler('stop', self.stop_game, pass_chat_data=True))
        self.dispatcher.add_handler(MessageHandler(Filters.reply, self.answer_handler, pass_chat_data=True))

    def answer_handler(self, update, context):
        chat_id = update.effective_chat.id
        message = update.message.text
        if message == 'A' or message == 'B' or message == 'C' or message == 'D':
            chat_active_game = self.db.get_active_game(chat_id)
            if chat_active_game is not None:
                status = chat_active_game["status"]
                if status == 'ingame':
                    user_id = update.message.from_user.id
                    user = self.db.get_player(user_id)

                    if user is None:
                        if update.message.from_user.username is None:
                            name = update.message.from_user.first_name
                        else:
                            name = update.message.from_user.username
                        self.db.add_player(user_id, name)
                        user = self.db.get_player(user_id)

                    if not self.db.is_player_in_game(user, chat_active_game):
                        self.db.add_player_to_game(user, chat_active_game)

                    self.db.add_answer(chat_active_game, user, message)

    def next_question(self, update, context):
        chat_id = update.effective_chat.id
        chat_active_game = self.db.get_active_game(chat_id)
        if chat_active_game is None:
            answer = 'no running game:\n' \
                     'create one with /newgame'
            self.bot.send_message(chat_id, answer)

        else:
            if chat_active_game is not None:
                status = chat_active_game["status"]
                if status == 'ingame':
                    answer = 'The answer was:\n' \
                             ''+chat_active_game["expected_answer"]+')' + self.db.get_answer_current_question(chat_active_game)
                    self.bot.send_message(chat_id, answer)
                    answer = 'score:\n'
                    for link in self.db.get_players_ingame(chat_active_game):
                        name = self.db.get_player(link._from.split("/")[1]).username
                        score = link["score"]
                        answer += '' + name + ':' + str(score) + '\n'
                    self.bot.send_message(chat_id, answer)

                    next_question= self.get_random_question()
                    print(next_question)
                    self.ask_question(chat_active_game,next_question)


    def stop_game(self, update, context):
        chat_id = update.effective_chat.id
        chat_active_game = self.db.get_active_game(chat_id)
        if chat_active_game is None:
            answer = 'no running game:\n' \
                     'create one with /newgame'
        else:
            self.db.end_game(chat_active_game)
            answer = 'stopping game:\n' \
                     'start a new one with /newgame'
        self.bot.send_message(chat_id, answer)

    def start_game(self, update, context):
        chat_id = update.effective_chat.id
        chat_active_game = self.db.get_active_game(chat_id)
        if chat_active_game is None:
            answer = 'Create a game first with /newgame'
            self.bot.send_message(chat_id, answer)

        else:
            status = chat_active_game["status"]
            if status == 'init':
                answer = 'Starting game:\n' \
                         'end it with /stop\n'\
                            'next question with /next'
                self.bot.send_message(chat_id, answer)
                first_question = self.get_random_question()
                self.db.start_game(chat_active_game)
                self.ask_question(chat_active_game, first_question)
            else:
                answer = 'Game already running:\n' \
                         'end it with /stop'
                self.bot.send_message(chat_id, answer)


    def new_game(self, update, context):
        chat_id = update.effective_chat.id

        chat_active_game = self.db.get_active_game(chat_id)

        if chat_active_game is None:
            self.db.add_new_game(chat_id)
            answer = 'Creating Game:\n' \
                     '/start to start the game'
        else:
            status = chat_active_game["status"]
            if status == 'init':
                answer = 'already Creating a Game:\n' \
                         '/start to start the game'
            else:
                answer = 'Game already running'
        self.bot.send_message(chat_id, answer)

        # q = Question(1, "comment", "oui", ["non", "ouais", "p-e"])
        # self.ask_question(chat_id, q)
        # update.message.reply_text(answer)

    def ask_question(self, game, question):

        question_doc = self.db.add_question(question)
        self.db.add_question_to_game(question_doc, game)
        self.db.set_current_question(game, question_doc)
        answers = question.wrong_answers
        answers.append(question.answer)
        random.shuffle(answers)

        text = 'Question:\n'
        text += question.question + '\n'
        letterAscii = 65
        for answer in answers:
            text += chr(letterAscii) + ')' + answer + '\n'
            if answer == question.answer:
                self.db.set_expected_answer(game, chr(letterAscii))
            letterAscii += 1
        self.bot.send_message(game['chat_id'], text, reply_markup=keyboard_markup())

    def create_game(self, chat_id):
        self.db.add(chat_id)

    def get_random_question(self):

        new_question = self.opentdb_client.get_questions(1, 0)[0]

        question = Question(new_question.question, new_question.correct_answer, new_question.incorrect_answers,
                            new_question.category)
        return question

    def add_question_to_game(self, question, game):

        question_doc = self.db.add_question(question)
        self.db.add_question_to_game(question_doc, game)
