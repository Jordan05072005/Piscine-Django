def my_var():
    i = 42
    print(i, "has a type", type(i))
    i = "42"
    print(i, "has a type", type(i))
    i = "quarante-deux"
    print(i, "has a type", type(i))
    i = 42.0
    print(i, "has a type", type(i))
    i = True
    print(i, "has a type", type(i))
    i = [42]
    print(i, "has a type", type(i))
    i = {42: 42}
    print(i, "has a type", type(i))
    i = (42,)
    print(i, "has a type", type(i))
    i = set()
    print(i, "has a type", type(i))





if __name__ == '__main__':
    my_var()
