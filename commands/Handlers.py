


def new_game(update, context):
    chat_id = update.effective_chat.id
    if chat_id in initGamesChat:
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
    update.message.reply_text(answer)


def join(update, context):
    chat_id = update.effective_chat.id
    if chat_id not in initGamesChat:
        answer='No available games:\n'
        '/newgame to start creating a game'
    else:
        answer= 'joining'
    update.message.reply_text(answer)
