from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, DateTime, Time, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from datetime import date, time

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, unique=True, nullable=False)

    subscription_time = Column(Time)

    #mensas saved in csv like: "mensa1,mensa2,mensa3"...
    #None if not subscribed
    subbed_mensas = Column(String, nullable=True)


class Food(Base):
    __tablename__ = "food"

    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    date = Column(Date, nullable=False, default=date.today())

    mensa_id = Column(Integer, ForeignKey("mensa.id"))
    mensa = relationship("Mensa", back_populates="foods")


class Mensa(Base):
    __tablename__ = "mensa"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)


class FoodRating(Base):
    __tablename__ = "foodrating"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False, default=date.today())
    rating = Column(Integer, nullable=False)

    user_id = Column(Integer, ForeignKey("user.chat_id"), nullable=False)
    user = relationship("User", back_populates="ratings")

    food_id = Column(Integer, ForeignKey("food.id"), nullable=False)
    food = relationship("Food", back_populates="ratings")
