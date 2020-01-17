from telegram import ReplyKeyboardMarkup


def keyboard_markup():
    keyboard = [["A", "B"], ["C", "D"]]

    repMkup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True)
    return repMkup
