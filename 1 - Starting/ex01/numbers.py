def readfile():
    filename = "numbers.txt"
    with open(filename, "r") as f:
        for line in f:
            elements = line.split(',')
            for element in elements:
                print(element.strip())


if __name__ == '__main__':
    readfile()