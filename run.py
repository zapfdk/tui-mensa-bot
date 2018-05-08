"""
This script sets up the bot with all the commands and jobs, and runs it.
"""

__author__ = "zapfdk"


import logging
import datetime as dt

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)

from res.strings import STRINGS
from src.db_handling import get_subbed_users, get_today_foods, add_rating, add_feedback, \
    gen_current_stats, add_stat, add_user, get_all_mensa_short_names, sub_user, unsub_user, get_user_by_chat_id, \
    has_user_voted_today
from src.parse_menu import get_today_menu
from src.config import TELEGRAM_API_TOKEN, ADMIN_ID


logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.ERROR)
logger = logging.getLogger(__name__)

DAYS = tuple(range(5))


"""
Commands
"""


def start(bot, update):
    """"
    Start mensa bot for this user and add him to user table.
    """
    update.message.reply_text(STRINGS["start"], parse_mode=ParseMode.MARKDOWN)
    add_user(chat_id=update.message.chat_id, subbed_mensas=None)


def get_help(bot, update):
    """
    Send help message to user.
    """
    update.message.reply_text(STRINGS["help"], parse_mode=ParseMode.MARKDOWN)


def sub(bot, update, args, job_queue, chat_data):
    """
    Add subscription and job for this user for given mensas in args.
    """
    subbed_mensas = conv_args_to_mensa_list(args)

    if not subbed_mensas:
        update.message.reply_text(STRINGS["sub"]["invalid_short_name"])
        return

    user = sub_user(chat_id=update.message.chat_id, subbed_mensas=subbed_mensas)

    #Remove job if available, else ignore
    try:
        job = chat_data["daily_job"]
        job.schedule_removal()
    except KeyError:
        pass

    chat_data["daily_job"] = job_queue.run_daily(daily_menu, time=user.subscription_time, days=DAYS, context=user.chat_id)
    update.message.reply_text(STRINGS["sub"]["success"].format(subbed_mensas=subbed_mensas), parse_mode=ParseMode.MARKDOWN)

def unsub(bot, update, chat_data):
    """
    Remove subscription and job for this user.
    """
    user = unsub_user(chat_id=update.message.chat_id)

    #Remove job if available, else ignore
    try:
        job = chat_data["daily_job"]
        job.schedule_removal()
    except KeyError as e:
        pass

    update.message.reply_text(STRINGS["unsub"]["success"], parse_mode=ParseMode.MARKDOWN)

def menu(bot, update, args):
    """
    Send today's menu to user.
    """
    mensa_list = conv_args_to_mensa_list(args)

    if not mensa_list:
        update.message.reply_text(STRINGS["sub"]["invalid_mensa_short_name"], parse_mode=ParseMode.MARKDOWN)
        return

    menu_txt = format_menu(mensa_list)

    update.message.reply_text(text=menu_txt, parse_mode=ParseMode.MARKDOWN)


def start_rating(bot, update):
    """
    Initiate Rating process and send food options from today.
    """
    if has_user_voted_today(update.message.chat_id):
        update.message.reply_text(STRINGS["rate"]["already_rated"])
        return

    # print(has_user_voted_today(update.message.chat_id))

    today_foods = get_today_foods()
    food_options = [[InlineKeyboardButton(food.description, callback_data=food.id)] for food in today_foods]

    food_list_markup = InlineKeyboardMarkup(food_options)
    update.message.reply_text(STRINGS["rate"]["choose_food"], reply_markup=food_list_markup)

    return 0


def handle_food_choice(bot, update, chat_data):
    """
    Handle food selection and send options for rating.
    """
    food_choice = update.callback_query
    chat_data["selected_food"] = food_choice.data

    rating_options = [[InlineKeyboardButton("{}".format(a), callback_data=a) for a in range(1, 6)]]
    rating_list_markup = InlineKeyboardMarkup(rating_options)

    update.callback_query.edit_message_text(STRINGS["rate"]["choose_rating"], reply_markup=rating_list_markup)

    return 1

def handle_food_rating(bot, update, chat_data):
    """
    Process and save rating of the food
    """
    rating_choice = update.callback_query

    add_rating(chat_id=update.callback_query.message.chat_id, food_id=chat_data["selected_food"], rating=rating_choice.data)

    del chat_data["selected_food"]

    update.callback_query.edit_message_text(STRINGS["rate"]["choose_rating"], reply_markup="")
    update.callback_query.answer(STRINGS["rate"]["thanks"])


def stats(bot, update):
    """
    Send current statistics to user.
    """
    current_stats = gen_current_stats()
    stat_msg = STRINGS["stats"].format(**current_stats)
    update.message.reply_text(stat_msg, parse_mode=ParseMode.MARKDOWN)


def feedback(bot, update, args):
    """
    Save feedback from user to the database.
    """
    if not args:
        update.message.reply_text(STRINGS["feedback"]["no_feedback"])
        return

    feedback_text = " ".join(args)
    add_feedback(chat_id=update.message.chat_id, feedback_text=feedback_text)
    bot.send_message(chat_id=ADMIN_ID, text="Neues Feedback: "+feedback_text)

    update.message.reply_text(STRINGS["feedback"]["thanks"], parse_mode=ParseMode.MARKDOWN)


def set_time(bot, update, args, chat_data):
    """
    Set subscription time for this user.
    """
    if not args:
        update.message.reply_text(STRINGS["time"]["wrong_arg"], parse_mode=ParseMode.MARKDOWN)
        return
    try:
        sub_time = dt.datetime.strptime(args[0], "%H:%M").time()
    except ValueError:
        update.message.reply_text(STRINGS["time"]["wrong_arg"], parse_mode=ParseMode.MARKDOWN)
        return

    user = sub_user(update.message.chat_id, subscription_time=sub_time)

    # Remove job if available, else ignore
    try:
        job = chat_data["daily_job"]
        job.schedule_removal()
    except KeyError:
        pass

    chat_data["daily_job"] = job_queue.run_daily(daily_menu, time=user.subscription_time, days=DAYS,
                                                 context=user.chat_id)

    update.message.reply_text(STRINGS["time"]["success"].format(sub_time=args[0]), parse_mode=ParseMode.MARKDOWN)


"""
Jobs
"""


def daily_menu(bot, job):
    """
    Send menu daily to user at subscription time.
    """
    chat_id = job.context

    user = get_user_by_chat_id(chat_id)
    mensa_list = user.subbed_mensas.split(",")

    menu_txt = format_menu(mensa_list)
    
    bot.send_message(chat_id=chat_id, text=menu_txt, parse_mode=ParseMode.MARKDOWN)


def get_menu(bot, job):
    """
    Download and scrape menu daily and save to database.
    """
    get_today_menu()


def log_stats(bot, job):
    """
    Daily job for logging statistics to database.
    """
    add_stat()


def handle_error(bot, update, error):
    """
    Simple warning logger.
    """
    logger.warning("Update %s caused error %s" %(update, error))


def setup_init_jobs_from_db(updater):
    """
    When script or service is restarted, reinitialize all jobs from database.
    """
    job_queue = updater.job_queue

    subbed_users = get_subbed_users()
    for subbed_user in subbed_users:
        chat_id = subbed_user.chat_id
        sub_time = subbed_user.subscription_time
        updater.dispatcher.chat_data[chat_id] = {}
        updater.dispatcher.chat_data[chat_id]["daily_job"] = \
            job_queue.run_daily(daily_menu, time=sub_time, context=chat_id, days=DAYS)


"""
MISC
"""


def format_menu(mensa_list):
    """
    Format menu into a readable form.
    """
    # print(mensa_list)
    today_foods = get_today_foods(mensa_list)

    # print(today_foods)

    if not list(today_foods):
        menu_txt = "Heute gibt es leider kein Essen in der Mensa."
        return menu_txt

    menu_txt = "Speiseplan für den {}\n\n".format(today_foods[0].date.strftime("%d.%m.%y"))

    current_mensa = ""

    for food in today_foods:
        if food.mensa.name != current_mensa:
            menu_txt += "\n*%s*\n" % food.mensa.name
            current_mensa = food.mensa.name
        menu_txt += "- %s (%.2f€)\n" % (food.description, food.price / 100)

    return menu_txt


def conv_args_to_mensa_list(args):
    """
    Convert argument list to csv-format which can be saved to database.
    """
    distinct_mensa_short_names = get_all_mensa_short_names()

    if not args:
        subbed_mensas = ",".join(distinct_mensa_short_names)
    elif any(arg not in distinct_mensa_short_names for arg in args):
        return 0
    else:
        subbed_mensas = ",".join(args)
    return subbed_mensas


if __name__ == "__main__":
    # Initialize Bot with API TOKEN
    updater = Updater(TELEGRAM_API_TOKEN)

    # Setup commands
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("help", get_help))
    updater.dispatcher.add_handler(CommandHandler("sub", sub, pass_chat_data=True, pass_job_queue=True, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler("unsub", unsub, pass_chat_data=True))
    updater.dispatcher.add_handler(CommandHandler("feedback", feedback, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler("menu", menu, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler("stats", stats))
    updater.dispatcher.add_handler(CommandHandler("time", set_time, pass_chat_data=True, pass_args=True))

    # Setup conversation handler for rating feature
    rating_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("rate", start_rating)],
        states={0: [CallbackQueryHandler(handle_food_choice, pass_chat_data=True)],
                1: [CallbackQueryHandler(handle_food_rating, pass_chat_data=True)]},
        fallbacks=[CommandHandler("rate", start_rating)]
    )
    updater.dispatcher.add_handler(rating_conv_handler)

    # Setup error handler which logs errors and warnings
    updater.dispatcher.add_error_handler(handle_error)

    # Setup jobs
    job_queue = updater.job_queue
    job_queue.run_daily(get_menu, dt.time(hour=1))
    job_queue.run_daily(log_stats, dt.time(hour=1))
    setup_init_jobs_from_db(updater)

    # Start
    updater.start_polling()
