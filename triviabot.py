from collections import Set

from telegram.ext import Updater, CommandHandler
from Bot.myBot import TriviaBot;
from Bot.Handlers import  join



def hello(update, context):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))



def main():

    triviaBot=TriviaBot('895779019:AAE54Vxeh5zWdhyy9rsywEVnMMeI8O1RW98')
    triviaBot.start()



if __name__ == '__main__':
    main()
