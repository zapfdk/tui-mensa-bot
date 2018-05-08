from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import date
from src.db_handling import add_food, get_mensa_id_from_name

MENU_LINK = "https://spi.tu-ilmenau.de/mensa"


def get_today_menu():
    r = urlopen(MENU_LINK).read()
    soup = BeautifulSoup(r, "html.parser")
    today_meals = soup.find("div", class_="content")

    mensa = soup.find("div", class_="mensa").find("h3")
    menu_date = mensa.get_text().split(" ")[1]
    today = date.today()

    if not (today.strftime("%d.%m.%Y") == menu_date):
        print("Kein Essen für heute.")
        return

    for idx, (mensa_foods, html_mensa) in enumerate(zip(today_meals.find_all("ul", class_="clearfix"),
                                                        today_meals.find_all("h4"))):
        mensa_name = html_mensa.get_text(strip=True)
        mensa_id = get_mensa_id_from_name(mensa_name)
        for meal_tag, price_tag in zip(mensa_foods.find_all("span", class_="meal"),
                                       mensa_foods.find_all("span", class_="price")):
            meal = meal_tag.get_text()
            price = price_tag.get_text(strip=True).strip("() €")
            price = price.replace(",", "")
            try:
                price = int(price)
            except ValueError:
                print("Kein Preis angegeben.")
                price = 0

            add_food(description=meal, price=price, food_date=date.today(), mensa_id=mensa_id)


if __name__ == "__main__":
    get_today_menu()