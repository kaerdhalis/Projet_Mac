from collections import Set

from telegram.ext import Updater, CommandHandler
from telegram.bot import Bot

from Bot.Handlers import new_game, join



def hello(update, context):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))



def main():
    updater = Updater('895779019:AAE54Vxeh5zWdhyy9rsywEVnMMeI8O1RW98', use_context=True)

    bot= Bot('895779019:AAE54Vxeh5zWdhyy9rsywEVnMMeI8O1RW98')

    updater.dispatcher.add_handler(CommandHandler('hello', hello))

    updater.dispatcher.add_handler(CommandHandler('newgame', new_game, pass_chat_data=True))
    updater.dispatcher.add_handler(CommandHandler('join', join, pass_chat_data=True))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
