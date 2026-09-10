import sys


def find_capital_city(city):
    states = {
        "Oregon" : "OR",
        "Alabama" : "AL",
        "New Jersey": "NJ",
        "Colorado" : "CO"
    }
    capital_cities = {
        "OR": "Salem",
        "AL": "Montgomery",
        "NJ": "Trenton",
        "CO": "Denver"
    }

    for (city_for_list, initial) in states.items():
        if city.lower() == city_for_list.lower():
            print(capital_cities[initial])
            return
    print("Unknown state")


if __name__ == '__main__':
    if len(sys.argv) != 2: sys.exit()
    find_capital_city(sys.argv[1])
