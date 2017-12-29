import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler

from .config import TELEGRAM_API_TOKEN
from .mensa_bot_strings import mensa_bot_strings
from .db_handling import get_subbed_users, get_today_foods, has_user_voted_today, add_rating, add_feedback, \
    gen_current_stats, add_stat, add_user, get_all_mensa_short_names, sub_user, unsub_user


logging.basicConfig(format="%asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)


"""
Commands
"""
def start(bot, update):
    update.message.reply_text(mensa_bot_strings["start"])
    add_user(chat_id=update.message.chat_id, subbed_mensas=None)


def help(bot, update):
    update.message.reply_text(mensa_bot_strings["help"])


def sub(bot, update, args, job_queue, chat_data):
    distinct_mensa_short_names = get_all_mensa_short_names()
    if any(short_name not in distinct_mensa_short_names for short_name in distinct_mensa_short_names):
        update.message.reply_text(mensa_bot_strings["invalid_mensa_short_name"] + ", ".join(distinct_mensa_short_names))
        return
    subbed_mensas = ",".join(args)
    sub_user(chat_id=update.message.chat_id, subbed_mensas=subbed_mensas)


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


def stats(bot, update):
    current_stats = gen_current_stats()
    stat_msg = "Aktuelle Statistiken:\n" \
               "{total_users} bisher gesehen Benutzer\n" \
               "{subbed_users} aktuelle Nutzer\n" \
               "{ratings} abgegebene Bewertungen\n".format(**current_stats)
    update.message.reply_text(stat_msg)


def feedback(bot, update, args):
    feedback_text = " ".join(args)
    add_feedback(chat_id=update.message.chat_id, feedback_text=" ".join(args))

    update.message.reply_text(mensa_bot_strings["thanks_for_feedback"])


"""
Jobs
"""
def daily_menu(bot, job):pass

def log_stats(bot, job):
    add_stat()

def init_daily_menus_from_db():pass



def handle_error(bot, update, error):
    logger.warning("Update %s caused error %s" %(update, error))


if __name__ == "__main__":
    updater = Updater(TELEGRAM_API_TOKEN)

    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("help", help))
    updater.dispatcher.add_handler(CommandHandler("sub", sub, pass_chat_data=True, pass_job_queue=True, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler("unsub", unsub, pass_chat_data=True))
    updater.dispatcher.add_handler(CommandHandler("feedback", feedback, pass_args=True))

    rating_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("rate", start_rating)],
        states={0: [CallbackQueryHandler(handle_food_choice)],
                1: [CallbackQueryHandler(handle_food_rating)]},
        fallbacks=[CommandHandler("rate", start_rating)]
    )
    updater.dispatcher.add_handler(rating_conv_handler)

    updater.dispatcher.add_error_handler(handle_error)

    updater.start_polling()