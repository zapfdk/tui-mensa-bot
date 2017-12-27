import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from .config import TELEGRAM_API_TOKEN

logging.basicConfig(format="%asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)

"""
Commands
"""
def start(bot, update):pass

def help(bot, update):pass

def sub(bot, update):pass

def unsub(bot, update):pass

def rate(bod, update):pass

def stats(bot, update):pass

def feedback(bot, update):pass


"""
Jobs
"""
def daily_menu(bot, update):pass

def log_stats(bot, update):pass


def handle_error(bot, update, error):
    logger.warning("Update %s caused error %s" %(update, error))


if __name__ == "__main__":
    updater = Updater(TELEGRAM_API_TOKEN)

    command_mapping = {"start": start,
                       "help": help,
                       "sub": sub,
                       "unsub": unsub,
                       "rate":rate}

    for command, callback in command_mapping.iteritems():
        updater.dispatcher.add_handler(CommandHandler(command, callback))




    updater.start_polling()