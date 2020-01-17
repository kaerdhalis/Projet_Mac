initGamesChat = set();
activeGamesChat = set();
from Bot.myBot import TriviaBot;


def create_game(chat_id):
    initGamesChat.add(chat_id)


def join(update, context):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))
