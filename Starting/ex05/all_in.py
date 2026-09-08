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
                    print(capital.capitalize(),"is the capital of", city)
                    return 1
    return 0


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
            print(capital_cities[initial],"is the capital of", city.capitalize())
            return 1
            return 1
    return 0



def all_in(argv):
    if ",," in argv:
        return
    words = argv.split(',')
    for word in words:
        if word.strip() == "":
            continue
        if find_city(word.strip()):
            continue
        elif find_capital_city(word.strip()):
            continue
        else:
            print(word.strip(), "is neither a capital city nor a state")

if __name__ == '__main__':
    if len(sys.argv) != 2: sys.exit()
    all_in(sys.argv[1])
