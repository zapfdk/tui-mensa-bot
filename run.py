import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from .config import TELEGRAM_API_TOKEN
from .mensa_bot_strings import mensa_bot_strings
from .db_handling import get_subbed_users, get_today_foods, has_user_voted_today, add_rating


logging.basicConfig(format="%asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)


"""
Commands
"""
def start(bot, update):
    update.message.reply_text(mensa_bot_strings["start"])


def help(bot, update):
    update.message.reply_text(mensa_bot_strings["help"])


def sub(bot, update):pass


def unsub(bot, update):pass


def start_rating(bot, update):
    """
    Initiate Rating process and send food options from today.
    """
    if has_user_voted_today():
        update.message.reply_text(mensa_bot_strings["already_voted"])
        return

    today_foods = get_today_foods()
    food_options = [[InlineKeyboardButton(food.description, callback_data=food.id) for food in today_foods]]

    food_list_markup = InlineKeyboardMarkup(food_options)
    update.message.reply_text(mensa_bot_strings["choose_food"], reply_markup=food_list_markup)


def handle_food_choice(bot, update, chat_data):
    """
    Handle food selection and send options for rating.
    """
    food_choice = update.callback.query
    chat_data["selected_food"] = food_choice.data

    rating_options = [[InlineKeyboardButton("%d Sterne" %(stars), callback_data=stars) for stars in range(1,6)]]
    rating_markup = InlineKeyboardMarkup(rating_options)
    update.message.reply_text(mensa_bot_strings["choose_rating"], reply_markup=rating_markup)


def handle_food_rating(bot, update, chat_data):
    """
    Process and save rating of the food
    """
    rating_choice = update.callback.query
    add_rating(chat_id=update.message.chat_id, food_id=chat_data["selected_food"], rating=rating_choice.data)

    del chat_data["selected_food"]

    update.message.reply_text(mensa_bot_strings["thanks_for_voting"])


def stats(bot, update):pass

def feedback(bot, update):pass


"""
Jobs
"""
def daily_menu(bot, job):pass

def log_stats(bot, job):pass

def init_daily_menus_from_db():pass



def handle_error(bot, update, error):
    logger.warning("Update %s caused error %s" %(update, error))


if __name__ == "__main__":
    updater = Updater(TELEGRAM_API_TOKEN)

    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("help", help))
    updater.dispatcher.add_handler(CommandHandler("sub", sub, pass_chat_data=True, pass_job_queue=True))
    updater.dispatcher.add_handler(CommandHandler("unsub", unsub, pass_chat_data=True))

    updater.dispatcher.add_handler(CommandHandler("rate", start_rating))
    updater.dispatcher.add_handler(CallbackQueryHandler())




    updater.start_polling()