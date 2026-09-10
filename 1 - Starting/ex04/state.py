import sys

def find_city(capital):
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
    for (initial, capital_list) in capital_cities.items():
        if capital.lower() == capital_list.lower():
            for (city, initial_city) in states.items():
                if initial == initial_city:
                    print(city)
                    return
    print("Unknown state")


if __name__ == '__main__':
    if len(sys.argv) != 2: sys.exit()
    find_city(sys.argv[1])
