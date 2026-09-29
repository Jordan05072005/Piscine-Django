from datetime import datetime

from django.conf import settings
from django.shortcuts import render, redirect
from .forms.forms import BasicForm

def getForm(request):
    if request.method == 'POST':
        form = BasicForm(request.POST)
        print("njnae", request.POST)
        if form.is_valid():
            text =  form.cleaned_data["text"]
            with settings.LOG_FILE.open("a") as f:
                f.write(f"{datetime.now()} -> {text}\n")
            return redirect("/ex02/")
    else:
        form = BasicForm()
    try:
        history = []
        with open(settings.LOG_FILE, encoding="utf-8") as f:
            history = f.read().splitlines()
    except FileNotFoundError:
        pass
    return render(request,'index.html', {
        'form': form,
        "history": history,
    })
