
def sort_lst(lst):
    if lst == []: return []
    pivot, lst_inf, lst_sup = lst[len(lst) - 1], [], []
    for i in range( 0 ,len(lst) - 1):
        if lst[i] < pivot:
            lst_inf.append(lst[i])
        else:
            lst_sup.append(lst[i])
    return sort_lst(lst_inf) + [pivot] + sort_lst(lst_sup)

def find_key(dic, value):
    keys = []
    for key, val in dic.items():
        if val == value:
            keys.append(key)
    return sort_lst(keys)

def my_sort_dico(dic):
    # list(mon_dico.items())[2]
    dic_lst = list(dic.items())
    values = list(dic.values())
    sort_values = sort_lst(values)
    new_dic = {}

    for sort_value in sort_values:
        if (sort_values.count(sort_value) > 1):
            keys = find_key(dic, sort_value)
            for key in keys:
                new_dic[key] = sort_value
        else:
            idx = values.index(sort_value)
            new_dic[dic_lst[idx][0]] = sort_value

    print(new_dic)




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
    print(my_sort_dico(d))