from django.shortcuts import render, redirect
from .models import Movies
from .forms.forms import RemoveMovie, UpdateMovie

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

def remove(request):
    try:
        titles = [(t, t) for t in Movies.objects.values_list("title", flat=True)]
        if request.method == "POST":
            form  = RemoveMovie(titles, request.POST)
            if form.is_valid():
                Movies.objects.filter(title=form.cleaned_data['title']).delete()
                return redirect("/ex07/remove")
        else:
            form = RemoveMovie(titles)
    except Exception as e:
        titles = []
        form = None
        print(e)
    return render(request, "form_ex07.html", {"form": form, "titles": titles, "buttonName": "Remove"})

def update(request):
    try:
        titles = [(t, t) for t in Movies.objects.values_list("title", flat=True)]
        if request.method == "POST":
            form  = UpdateMovie(titles, request.POST)
            if form.is_valid():
                movie = Movies.objects.get(title=form.cleaned_data["title"])
                movie.opening_crawl = form.cleaned_data["opening_crawl"]
                movie.save()
                return redirect("/ex07/update")
        else:
            form = UpdateMovie(titles)
    except Exception as e:
        titles = []
        form = None
        print(e)
    return render(request, "form_ex07.html", {"form": form, "titles": titles, "buttonName": "Update"})