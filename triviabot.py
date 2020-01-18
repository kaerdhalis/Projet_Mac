from collections import Set

from telegram.ext import Updater, CommandHandler
from Bot.myBot import TriviaBot;
from Bot.Handlers import join


def main():
    trivia_bot = TriviaBot('895779019:AAE54Vxeh5zWdhyy9rsywEVnMMeI8O1RW98')
    trivia_bot.start()


if __name__ == '__main__':
    main()
