from django.shortcuts import render
from .forms.forms import FormMovie
from .models import Movies, People, Planets

# Create your views here.
def display(request):
    gender_choice = People.objects.values('gender').distinct()
    rows = []
    header = []
    try:
        if request.method == 'POST':
            form = FormMovie(gender_choice, request.POST)
            if form.is_valid():
                rows = (
                    Movies.objects
                    .filter(characters_gender=form.cleaned_data['gender'],
                            release_date__range=[form.cleaned_data['date_min'], form.cleaned_data['date_max']],
                            characters_homeworld_diameter__gte=form.cleaned_data['homeworld_diameter'])
                    # .order_by("name")
                    .values_list("characters__name", "characters__gender", "title", "characters_homeworld", "characters_homeworld_diameter")
                )
                if rows and len(rows) > 0:
                    header = ["Character Name", "Character Gender", "Movie Title", "Character Homeworld", "Character Homeworld Diameter"]
        else:
            form = FormMovie(gender_choice)
    except Exception as e:
        print(e)
        form = None
    return render(request, "display_ex10.html", {"form": form, "rows": rows, "header": header})