import sys, re


def parsing_settings():
    dic = {}
    try:
        with open('settings.py', 'r') as file:
            for line in file:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    dic[key.strip()] = value.strip().strip('"')
    except FileNotFoundError:
        print("Le fichier settings.py n'existe pas")
    return dic

# def get_args(line):
#     lst = []
#     i = 0
#     while i < len(line):
#         idx = line[i:].find('{')
#         idx_end = line[i:].find('}')
#         if idx != -1 and idx_end != -1:
#             lst.append(line[i:][idx+1:idx_end])
#             i+= (idx_end + 1)
#         else:
#             break
#     return lst

def get_args(line):
    lst = re.findall(r"\{(\w+)\}", line)
    return lst


def create_cv(filename):
    if filename.split('.')[-1] != 'template':
        print("Le fichier n'est pas un template")
        return
    dic = parsing_settings()
    try:
        with open('file.html', 'w') as html:
            html.write('''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CV</title>
    <style>
    </style>
</head>
<body>
''')
            with open(filename) as f:
                for line in f:
                    for arg in get_args(line):
                        line = line.replace(f"{{{arg}}}", dic.get(arg, f"{{{arg}}}"))
                    html.write(line)
            html.write('</body>\n'
                    '</html>\n')
    except FileNotFoundError:
        print("Le fichier", filename,"n'existe pas")




if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Mauvais nombre d'arguments")
    else:
        create_cv(sys.argv[1])