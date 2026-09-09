import sys


def file_to_lst_dico(filename):
    elements = []
    with open(filename, 'r') as f2:
        for line in f2:
            line_split = line.split('=')
            elements.append({"element": line_split[0].strip()})
            for attribute in line_split[1].split(','):
                attribute_split = attribute.strip().split(':')
                elements[len(elements) - 1][attribute_split[0]] = attribute_split[1]
    print(elements)
    return elements



def write_html():
    lst = file_to_lst_dico('periodic_table.txt')
    with open('periodic_table.html', 'w') as f:
        f.write('''<!DOCTYPE html>\n<html lang="fr">\n<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Periodic Table</title>
    <style>
        body {
            padding: 50px;
            box-sizing: border-box;
            display: flex;
            justify-content: center;
        }
        div {
            max-width: 100%;
            overflow-x: auto;
        }
        table {
            border-collapse: collapse;
        }
        h1, h2, h3{
		    text-align: center;
		}
    </style>
</head>
<body>
\t<div>
\t\t<h1>Periodic Table</h1>
\t\t<h2>by Dmitri Mendeleïev</h2>
\t\t<h3>in 1869</h3>
\t\t<table>\n''')
        i = 0
        while i < len(lst):
            f.write('\t\t\t<tr>\n')
            for length in range(0, 18):
                if int(lst[i]["position"]) != length:
                    f.write('\t\t\t\t<td style="border: 1px solid black; padding:10px"></td>\n')
                    continue

                f.write(f'\t\t\t\t<td style="border: 1px solid black; padding:10px">\n'
                              f'\t\t\t\t\t<h4> {lst[i]["element"]} </h4>\n'
                            '\t\t\t\t\t<ul>\n'
                                f'\t\t\t\t\t\t<li>No {lst[i]["position"]} </li>\n'
                                f'\t\t\t\t\t\t<li> {lst[i]["small"]} </li>\n'
                                f'\t\t\t\t\t\t<li> {lst[i]["molar"]} </li>\n'
                                f'\t\t\t\t\t\t<li> {lst[i]["electron"]} electron</li>\n'
                            '\t\t\t\t\t</ul>\n'
                        '\t\t\t\t</td>\n'
                        )
                i+=1
            f.write('\t\t\t</tr>\n')
        f.write('\t\t</table>\n'
                '\t</div>\n'
                '</body>\n'
                '</html>\n')

if __name__ == '__main__':
    write_html()