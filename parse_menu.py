from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import date

from db_handling import add_food

MENU_LINK = "https://spi.tu-ilmenau.de/mensa"

def get_today_menu():
    r = urlopen(MENU_LINK).read()
    soup = BeautifulSoup(r, "html.parser")

    today_meals = soup.find("div", class_="content")

    today = date.today()
    menu_date = 0 #TODO

    for html_mensa in today_meals.find_all("h4"):
        pass

    for idx, mensa in enumerate(today_meals.find_all("ul", class_="clearfix")):

        for meal, price in zip(mensa.find_all("span", class_="meal"), mensa.find_all("span", class_="price")):
            add_food(description=meal.get_text(), price=)#TODO)
