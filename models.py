from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, DateTime, Time, Boolean, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

import datetime as dt

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger, unique=True, nullable=False)

    subscription_time = Column(Time, default=dt.time(hour=11))

    #mensas saved in csv like: "mensa1,mensa2,mensa3"...
    #None if not subscribed
    subbed_mensas = Column(String(128), nullable=True)

    feedbacks = relationship("Feedback", back_populates="user")
    ratings = relationship("FoodRating", back_populates="user")


class Food(Base):
    __tablename__ = "food"

    id = Column(Integer, primary_key=True)
    description = Column(String(256), nullable=False)
    price = Column(Integer, nullable=False)
    date = Column(Date, nullable=False, default=dt.date.today())

    mensa_id = Column(Integer, ForeignKey("mensa.id"), nullable=False)
    mensa = relationship("Mensa", back_populates="foods")

    ratings = relationship("FoodRating", back_populates="food")


class Mensa(Base):
    __tablename__ = "mensa"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    short_name = Column(String(8), nullable=False)

    foods = relationship("Food", back_populates="mensa")


class FoodRating(Base):
    __tablename__ = "foodrating"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False, default=dt.date.today())
    rating = Column(Integer, nullable=False)

    user_id = Column(BigInteger, ForeignKey("user.chat_id"), nullable=False)
    user = relationship("User", back_populates="ratings")

    food_id = Column(Integer, ForeignKey("food.id"), nullable=False)
    food = relationship("Food", back_populates="ratings")

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, default=dt.datetime.now(), nullable=False)
    feedback_text = Column(String(1024), nullable=False)

    user_id = Column(BigInteger, ForeignKey("user.chat_id"), nullable=False)
    user = relationship("User", back_populates="feedbacks")

class Stat(Base):
    __tablename__ = "stat"

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, default=dt.datetime.now(), nullable=False)
    total_users = Column(Integer, nullable=False)
    subbed_users = Column(Integer, nullable=False)
    ratings = Column(Integer, nullable=False)

if __name__ == "__main__":
    Base.metadata.create_all()