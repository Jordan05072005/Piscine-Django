import sys, requests
from bs4 import BeautifulSoup

def roads_to_philosophy(title, arr=None):
    if arr is None:
        arr = []
    headers = {
        "User-Agent": "MonScraper/1.0 (contact: mon.email@example.com)"
    }
    r = requests.get(f"https://en.wikipedia.org/wiki/{title}", headers=headers)
    if r.status_code != 200:
        return print("It's a dead end !")
    soup = BeautifulSoup(r.text, "html.parser")
    title = soup.select_one("title").get_text().replace(" - Wikipedia", "")
    print(title)
    if title == "Philosophy": return print(f"{len(arr)} roads from {arr[0]} to philosophy !")
    intro = soup.select_one("section[data-mw-section-id='0']")
    name = None
    for p in intro.find_all("p", recursive=False):
        for a in p.find_all("a", href=True):
            name = a.get("href").split("wiki/")[-1]
            if name == title or name.startswith("Help:") or name.startswith("#"):
               name = None
               continue
            if name in arr :
               print("It leads to an infinite loop !")
               return 1
            break
        if name:
            break
    if name:
        arr.append(title)
        return roads_to_philosophy(name, arr)
    return print("It leads to a dead end !")



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 roads_to_philosophy.py <title>")
    else:
        roads_to_philosophy(sys.argv[1])