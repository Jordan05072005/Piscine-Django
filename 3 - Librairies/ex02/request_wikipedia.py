from string import whitespace

import requests
import json, dewiki, sys

def parsing(json):
    pages = json["query"]["pages"]
    page = next(iter(pages.values()))
    if "revisions" in page:
        return page["revisions"][0]["slots"]["main"]["*"]
    return None

# {{date|17 février 2015}}

def clean_file(text):
    replace = ["[[", "]]", "'''"]
    cara = {"{{": "}}", "<ref": "</ref>", "<re": "/>",  "Fichier": "\n"}
    list_data=["date", "nobr", "Citation", "unité", "nb"]
    for (key, value) in cara.items():
        lst, i = [], 0
        while i < len(text):
            idx = text[i:].find(key)
            if idx == -1: break
            lst.append(i + idx)
            i += (idx + len(key))
        for i in range(len(lst) - 1, -1, -1):
            idx2 = text[lst[i]:].find(value)
            if idx2 == -1: continue
            d = text[lst[i]:lst[i] + idx2 + len(value)]
            split = d.split("|")
            if key == "{{" and split[0].strip('{') in list_data:
                text = text[:lst[i]] + split[-1].strip('}') + text[lst[i] + idx2 + len(value):]
            else:
                text = text[:lst[i]] + text[lst[i] + idx2 + len(value):]
    for r in replace:
        text = text.replace(r, "")
    # text = dewiki.from_string(text)
    return text

def request_wikipedia(title):
    lang = 'fr'
    url = f"https://{lang}.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "titles": title,
        "prop": "revisions",
        "rvprop": "content",
        "rvslots": "main",
        "format": "json",
    }
    headers = {
        "User-Agent": "MonScript42/1.0 (jordan@example.com)"
    }
    r = requests.get(url, params=params, headers=headers)
    if r.status_code != 200:
        return print("Error: Status code invalid.")
    data_parsing = parsing(r.json())
    if not data_parsing:
        return print("Error: No data found.")
    data = clean_file(data_parsing)
    if "#REDIRECT" in data or "#redirect" in data:
        return request_wikipedia(data[len("#REDIRECT"):].strip())
    with open(f"{title.replace(' ', '_')}.wiki", "w") as f:
        f.write(data)
    return data



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Function need one argument.")
    else:
        request_wikipedia(sys.argv[1])