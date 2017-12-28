from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import DB_PASSWORD, DB_SYSTEM, DB_URL, DB_USERNAME
from .models import User, Food, FoodRating, Mensa

from datetime import date

db_config = "{0}://{1}:{2}@{3}".format(DB_SYSTEM, DB_USERNAME, DB_PASSWORD, DB_URL)
db_engine = create_engine(db_config)
Session = sessionmaker(bind=db_engine)

sess = Session()

def add_user(chat_id, subscribed):
    user = User(chat_id=chat_id, subscribed=subscribed)

    add_entity(user)

def add_food(description, price, date, **mensa_info):
    mensa_id = sess.query(Mensa).filter_by(**mensa_info).first().id
    food = Food(description=description, price=price, date=date, mensa_id=mensa_id)

    add_entity(food)

def add_mensa(name, short_name):
    mensa = Mensa(name=name, short_name=short_name)

    add_entity(mensa)

def add_rating(chat_id, food_id, rating, date=date.today()):
    rating = FoodRating(date=date, user_id=chat_id, food_id=food_id, rating=rating)

    add_entity(rating)

def add_entity(entity):
    assert(isinstance(entity, (User, Food, FoodRating, Mensa)))

    sess.add(entity)
    sess.commit()

def get_today_foods():
    today = date.today()

    today_foods = list(sess.query(Food).filter_by(date=today))
    return today_foods

def get_subbed_users():
    subbed_users = list(sess.query(User).filter(User.subbed_mensas != None))

    return subbed_users

def has_user_voted_today(chat_id):
    found_rating = sess.query(FoodRating).filter_by(chat_id=chat_id, date=date.today()).first()
    return found_rating





