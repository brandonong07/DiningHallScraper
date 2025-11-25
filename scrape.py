import requests
import pprint
from bs4 import BeautifulSoup

URL = "https://housing.ucdavis.edu/dining/dining-commons/tercero/"

headers = {
    "User-Agent": "Mozilla/5.0 (menu-scraper-tutorial)"
}

resp = requests.get(URL, headers=headers)
resp.raise_for_status()

soup = BeautifulSoup(resp.text, "html.parser")

days = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"}
meals = {"Breakfast", "Lunch", "Dinner"}

current_day = None
current_meal = None
current_zone = None

rows = []
menu = {}

for tag in soup.find_all(["h1", "h2", "h3", "h4"]):
    text = tag.get_text(strip=True)

    # Day header: "# Sunday", "# Monday", ...
    if tag.name == "h1" and text in days:
        current_day = text
        current_meal = None
        current_zone = None
        continue

    # Meal header: "## Breakfast", "## Lunch", "## Dinner"
    if tag.name == "h2" and text in meals:
        current_meal = text
        current_zone = None
        continue

    # Zone header: "### Red Zone", "### Yellow Zone", ...
    if tag.name == "h3" and text.endswith("Zone"):
        current_zone = text.replace(" Zone", "")
        continue

    # Dish line: "#### Omelette||Fried Egg||Scrambled Eggs/Tofu", etc.
    if tag.name == "h4":
        dish = text
        if "Currently there are no dishes" in dish:
            continue
        if current_day and current_meal and current_zone:
            # Create day entry if missing
            if current_day not in menu:
                menu[current_day] = {}

            # Create meal entry if missing
            if current_meal not in menu[current_day]:
                menu[current_day][current_meal] = {}

            # Create zone entry if missing
            if current_zone not in menu[current_day][current_meal]:
                menu[current_day][current_meal][current_zone] = []

            # Append dish to list
            menu[current_day][current_meal][current_zone].append(dish)


# Quick sanity check

day = input("Enter day (e.g., Monday): ").strip().capitalize()
meal = input("Enter meal (Breakfast, Lunch, Dinner): ").strip().capitalize()

def print_meal(menu, day, meal):
    if day in menu and meal in menu[day]:
        pprint.pprint(menu[day][meal])
    else:
        print(f"No data available for {meal} on {day}.")

print_meal(menu, day, meal)

