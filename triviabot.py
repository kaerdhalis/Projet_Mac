from collections import Set

from telegram.ext import Updater, CommandHandler

from commands.Handlers import new_game, join

initGamesChat = set();
activeGamesChat = set();


def hello(update, context):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))






def create_game(chat_id):
    initGamesChat.add(chat_id)




updater = Updater('895779019:AAE54Vxeh5zWdhyy9rsywEVnMMeI8O1RW98', use_context=True)

updater.dispatcher.add_handler(CommandHandler('hello', hello))

updater.dispatcher.add_handler(CommandHandler('newgame', new_game, pass_chat_data=True))
updater.dispatcher.add_handler(CommandHandler('join', join, pass_chat_data=True))
updater.start_polling()
updater.idle()
