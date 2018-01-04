"""
This file contains several helper functions for adding and retrieving data to/from the database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from config import DB_PASSWORD, DB_SYSTEM, DB_URL, DB_USERNAME, DB_DATABASE_NAME
from models import User, Food, FoodRating, Mensa, Feedback, Stat, Base

from datetime import date, datetime, time

db_config = "{0}://{1}:{2}@{3}/{4}".format(DB_SYSTEM, DB_USERNAME, DB_PASSWORD, DB_URL, DB_DATABASE_NAME)
print(db_config)
db_engine = create_engine(db_config)
Session = sessionmaker(bind=db_engine)

sess = Session()

"""
Adding into tables
"""
def add_user(chat_id, subbed_mensas=None):
    user = User(chat_id=chat_id, subbed_mensas=subbed_mensas)

    add_entity(user)

def add_food(description, price, date, mensa_id):
    food = Food(description=description, price=price, date=date, mensa_id=mensa_id)

    add_entity(food)

def add_mensa(name, short_name):
    mensa = Mensa(name=name, short_name=short_name)

    add_entity(mensa)

def add_rating(chat_id, food_id, rating, date=date.today()):
    rating = FoodRating(date=date, user_id=chat_id, food_id=food_id, rating=rating)

    add_entity(rating)

def add_feedback(chat_id, feedback_text):
    feedback = Feedback(user_id=chat_id, feedback_text=feedback_text)

    add_entity(feedback)

def add_stat():
    current_stats = gen_current_stats()
    stat = Stat(**current_stats)

    add_entity(stat)

def add_entity(entity):
    assert(isinstance(entity, (User, Food, FoodRating, Mensa, Feedback, Stat)))

    try:
        sess.add(entity)
        sess.commit()
    except IntegrityError as e:
        sess.rollback()
        print(e.args, e.detail)

"""
Selecting from tables
"""
def get_today_foods(mensa_list=None):
    today = date.today()

    today_foods = sess.query(Food).filter_by(date=today)

    #If mensas were specified filter foods by them
    if mensa_list:
        today_foods = today_foods.filter(Food.mensa.short_name.in_(mensa_list))

    return today_foods

def get_subbed_users():
    subbed_users = list(sess.query(User).filter(User.subbed_mensas != None))

    return subbed_users

def get_user_by_chat_id(chat_id):
    user = sess.query(User).filter_by(chat_id=chat_id).first()

    return user

"""
Alter data in table
"""
def sub_user(chat_id, subbed_mensas, subscription_time=time(hour=11)):
    user = sess.query(User).filter_by(chat_id=chat_id).first()
    if not user:
        add_user(chat_id=chat_id, subbed_mensas=subbed_mensas)
        return
    user.subbed_mensas = subbed_mensas
    user.subscription_time = subscription_time
    try:
        sess.commit()
    except IntegrityError as e:
        sess.rollback()

    return user

def unsub_user(chat_id):
    user = sess.query(User).filter_by(chat_id=chat_id)
    if not user:
        add_user(chat_id=chat_id, subbed_mensas=None)
        return
    user.subbed_mensas = None
    try:
        sess.commit()
    except IntegrityError as e:
        sess.rollback()

    return user

"""
Miscellaneous from database
"""
def gen_current_stats():
    nb_total_users = sess.query(User).count()
    nb_subbed_users = sess.query(User).filter(User.subbed_mensas != None).count()
    nb_ratings = sess.query(FoodRating).count()

    stats = {"total_users": nb_total_users, "subbed_users": nb_subbed_users, "ratings": nb_ratings}
    return stats

def has_user_voted_today(chat_id):
    found_rating = sess.query(FoodRating).filter_by(user_id=chat_id, date=date.today()).first()
    return found_rating

def get_all_mensa_short_names():
    distinct_short_names = [str(short_name[0]) for short_name in sess.query(Mensa.short_name).distinct()]
    return distinct_short_names

def get_mensa_id_from_name(name):
    mensa = sess.query(Mensa).filter_by(name=name).first()
    return mensa.id

if __name__ == "__main__":
    Base.metadata.create_all(db_engine)
    # add_stat()


