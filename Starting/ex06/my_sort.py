
def sort_lst(lst, key=lambda x:x[0], value=lambda x: x[1]):
    if not lst:
        return []
    pivot = lst[len(lst) - 1]
    lst_inf = [x for x in lst[:-1] if value(x) < value(pivot) or (value(x) == value(pivot) and key(x) < key(pivot))]
    lst_sup = [x for x in lst[:-1] if value(x) > value(pivot) or (value(x) == value(pivot) and key(x) > key(pivot))]
    return sort_lst(lst_inf, key, value) + [pivot] + sort_lst(lst_sup, key, value)

def my_sort_dico(dic):
    items = sort_lst(list(dic.items()),  lambda item: item[0], lambda item: item[1])
    for name in dict(items).keys():
        print(name)


if __name__ == '__main__':
    d = {
        'Hendrix' : '1942',
        'Allman' : '1946',
        'King' : '1925',
        'Clapton' : '1945',
        'Johnson' : '1911',
        'Berry' : '1926',
        'Vaughan' : '1954',
        'Cooder' : '1947',
        'Page' : '1944',
        'Richards' : '1943',
        'Hammett' : '1962',
        'Cobain' : '1967',
        'Garcia' : '1942',
        'Beck' : '1944',
        'Santana' : '1947',
        'Ramone' : '1948',
        'White' : '1975',
        'Frusciante' : '1970',
        'Thompson' : '1949',
        'Burton' : '1939',
    }
    my_sort_dico(d)