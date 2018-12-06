import json
import datetime
import random
from enum import Enum

class Weekday(Enum):
    SUNDAY = 0
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6

restaurants = {}
preferences = {}

people_going = input("Who's going? (separated by spaces)\n").split(" ")

restaurants_file = "./restaurants.json"
preferences_file = "./preferences.json"

with open(restaurants_file) as json_file:
    restaurants = json.load(json_file)

with open(preferences_file) as json_file:
    preferences = json.load(json_file)

today = datetime.datetime.today().isoweekday()

preferences_going = {}

# Filter preferences by people going
for person_name, person_preferences in preferences.items():
    if (person_name in people_going):
        preferences_going[person_name] = person_preferences

valid_restaurant_names = []
valid_restaurant_weights = []

# Filter and weigh restaurants
for restaurant_name, restaurant_data in restaurants.items():
    # Filter restaurants that are closed
    is_open = False
    for open_day in restaurant_data["open"]:
        if Weekday(today).name == open_day.upper():
            is_open = True

    if not (is_open):
        continue

    is_vetoed = False
    net_weight = 0
    weight_modifier = 1/len(preferences_going)
    for person_name, person_preferences in preferences_going.items():
        # Filter vetoed restaurants
        if (restaurant_name in person_preferences["veto"]):
            is_vetoed = True
            break
        if (restaurant_data["cuisine"] in person_preferences["veto"]):
            is_vetoed = True
            break

        # Add and Subtract weights based on preferences
        # Things you dislike about a place probably outweigh things you like
        if (restaurant_name in person_preferences["dislike"] or restaurant_data["cuisine"] in person_preferences["dislike"]):
            net_weight -= weight_modifier
        if (restaurant_name in person_preferences["prefer"] or restaurant_data["cuisine"] in person_preferences["prefer"]):
            net_weight += weight_modifier
    
    if (is_vetoed):
        continue

    valid_restaurant_names.append(restaurant_name)
    valid_restaurant_weights.append(net_weight + 1)

# Get a random restaurant based on weight

random_restaurant = random.choices(valid_restaurant_names, valid_restaurant_weights)
print(random_restaurant[0])