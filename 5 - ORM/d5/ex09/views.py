from django.shortcuts import render
from .models import Planets, People

# Create your views here.


def display(request):
    header = []
    try:
        rows = (
            People.objects
            .filter(homeworld__climate__contains="windy")
            .order_by("name")
            .values_list("name", "homeworld__name", "homeworld__climate")
        )
        if rows and len(rows) > 0:
            header = ["name", 'homeworld', "climate"]
    except Exception as e:
        print(e)
        rows = []
    return render(request, "display_ex09.html", {"header" : header ,
                                                 "rows": rows,
                                                 "empty_mess":
                                                     "No data available, please use the following command line before use:\n"
                                                     "python3 manage.py load_ex09 ex09/ressources/ex09_initial_data.json"})

