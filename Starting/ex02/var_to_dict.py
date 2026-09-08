def var_to_dict(var):
    if (type(var) is not list): return
    d = {}
    for element in var:
        if (len(element) != 2): return
        d[element[1]] = element[0]
    # d = dict(sorted(d.items(), reverse = True))
    for (key, value) in d.items():
        print(key, ":" ,value)


if __name__ == '__main__':
    d = [
        ('Hendrix' , '1942'),
        ('Allman' , '1946'),
        ('King' , '1925'),
        ('Clapton' , '1945'),
        ('Johnson' , '1911'),
        ('Berry' , '1926'),
        ('Vaughan' , '1954'),
        ('Cooder' , '1947'),
        ('Page' , '1944'),
        ('Richards' , '1943'),
        ('Hammett' , '1962'),
        ('Cobain' , '1967'),
        ('Garcia' , '1942'),
        ('Beck' , '1944'),
        ('Santana' , '1947'),
        ('Ramone' , '1948'),
        ('White' , '1975'),
        ('Frusciante', '1970'),
        ('Thompson' , '1949'),
        ('Burton' , '1939')
    ]
    var_to_dict(d)



