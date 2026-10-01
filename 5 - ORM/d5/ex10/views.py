from django.shortcuts import render
from .forms.forms import FormMovie
from .models import Movies, People, Planets

# Create your views here.
def display(request):
    gender_choice = [
        (g, g)
        for g in People.objects.values_list("gender", flat=True).distinct().order_by("gender")
        if g
    ]
    rows = []
    header = []
    try:
        if request.method == 'POST':
            form = FormMovie(gender_choice, request.POST)
            if form.is_valid():
                rows = list(
                    Movies.objects
                    .filter(characters__gender=form.cleaned_data['gender'],
                            release_date__range=[form.cleaned_data['date_min'], form.cleaned_data['date_max']],
                            characters__homeworld__diameter__gte=form.cleaned_data['diameter'])
                    # .order_by("name")
                    .values_list("title", "characters__name", "characters__gender" , "characters__homeworld", "characters__homeworld__diameter")
                )
                if rows and len(rows) > 0:
                    header = ["Movie Title", "Character Name", "Character Gender" , "Character Homeworld", "Character Homeworld Diameter"]
        else:
            form = FormMovie(gender_choice)
    except Exception as e:
        print("ERROR: ", e)
        form = None
    return render(request, "display_ex10.html", {"form": form, "rows": rows, "header": header})