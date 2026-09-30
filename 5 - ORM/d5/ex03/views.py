from django.shortcuts import render
from .models import Movies

MOVIES = [
    (1, "The Phantom Menace", "George Lucas", "Rick McCallum", "1999-05-19"),
    (2, "Attack of the Clones", "George Lucas", "Rick McCallum", "2002-05-16"),
    (3, "Revenge of the Sith", "George Lucas", "Rick McCallum", "2005-05-19"),
    (4, "A New Hope", "George Lucas", "Gary Kurtz, Rick McCallum", "1977-05-25"),
    (5, "The Empire Strikes Back", "Irvin Kershner", "Gary Kutz, Rick McCallum", "1980-05-17"),
    (6, "Return of the Jedi", "Richard Marquand", "Howard G. Kazanjian, George Lucas, Rick McCallum", "1983-05-25"),
    (7, "The Force Awakens", "J. J. Abrams", "Kathleen Kennedy, J. J. Abrams, Bryan Burk", "2015-12-11"),
]

def populate(request):
    results = []
    for movie in MOVIES:
        try:

            Movies.objects.create(
                episode_nb = movie[0],
                title = movie[1],
                director = movie[2],
                producer = movie[3],
                release_date = movie[4],
            )
            results.append("OK")
        except Exception as e:
            results.append(str(e))
    return render(request, "index2.html", {"message": results})

def display(request):
    rows = []
    header = []
    try:
        header = [f.name for f in Movies._meta.fields]
        rows = list(Movies.objects.values_list())
    except Exception as e:
        print(e)
    return render(request, "displayORM.html", {"header" : header ,"rows": rows})
