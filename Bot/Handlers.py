initGamesChat = set();
activeGamesChat = set();
from Bot.myBot import AskQuestion

def create_game(chat_id):
    initGamesChat.add(chat_id)


def new_game(update, context):
    chat_id = update.effective_chat.id
    """if chat_id in initGamesChat:
        answer = 'Already creating Game:\n'
        '/join to join the game\n'
        '/start to start the game'
    elif chat_id in activeGamesChat:
        answer = 'Game already running'
    else:
        create_game(chat_id)
        answer = 'Creating Game:\n'
        '/join to join the game\n'
        '/start to start the game'
        """
    AskQuestion(update,None)
    #update.message.reply_text(answer)


def join(update, context):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))



