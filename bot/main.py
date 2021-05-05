from telegram_bot import *

if __name__ == '__main__':
    bot = Bot()
    bot.bot.polling(none_stop=True)