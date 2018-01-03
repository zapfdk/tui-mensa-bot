from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import date

from db_handling import add_food, get_mensa_id_from_name

MENU_LINK = "https://spi.tu-ilmenau.de/mensa"

def get_today_menu():
    r = urlopen(MENU_LINK).read()
    soup = BeautifulSoup(r, "html.parser")

    today_meals = soup.find("div", class_="content")

    today = date.today()
    menu_date = 0 #TODO

    for html_mensa in today_meals.find_all("h4"):
        pass

    for idx, (mensa_foods, html_mensa) in enumerate(zip(today_meals.find_all("ul", class_="clearfix"), today_meals.find_all("h4"))):
        mensa_name = html_mensa.get_text()
        mensa_id = get_mensa_id_from_name(mensa_name)
        for meal_tag, price_tag in zip(mensa_foods.find_all("span", class_="meal"), mensa_foods.find_all("span", class_="price")):
            meal = meal_tag.get_text()
            price = price_tag.get_text().strip("()€ ")
            price = int(price.replace(",",""))

            print(mensa_name, mensa_id, meal, price)

            add_food(description=meal, price=price, date=date.today(), mensa_id=mensa_id)#TODO


if __name__ == "__main__":
    get_today_menu()