import time, random
from django.conf import settings
from django.db import IntegrityError
from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm, TipForm
from .models import Tip, User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate


# Create your views here.

def home(request):
    print(request.user.is_authenticated, request.user)
    if not request.user.is_authenticated:
        now = time.time()
        if "name" not in request.session or now >= request.session.get("name_expire_at", 0):
            request.session["name"] = random.choice(settings.STATICS_NAMES)
            request.session["name_expire_at"] = now + 42

        remaining = int(request.session["name_expire_at"] - now) + 1
        name = request.session["name"]
        reputation = 0
    else:
        remaining = 0
        name = request.user.username
        reputation = request.user.reputation
    return render(request, 'welcome.html', {
        "name": name,
        "reputation": reputation,
        "remaining": remaining,
        "connected": request.user.is_authenticated
    })

def signup(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                print("Merde", User.objects.filter(username=form.cleaned_data['username']))
                user = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                login(request, user)
                return redirect('/')

            except IntegrityError:
                form.add_error('username', 'Error connecting to database')
        else:
            form.add_error('username', 'Username already exists')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def loginView(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('/')
            form.add_error(None, 'Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logoutView(request):
    if request.method == 'POST' and request.POST.get("logout") == "logout":
        logout(request)
        return redirect('/')
    return render(request, 'logout.html')


#--------------CRUD-----------------------------------

def create_tip(request):
    if request.method == 'POST':
        form = TipForm(request.POST)
        if form.is_valid():
            try:
                Tip.objects.create(author=request.user, content=form.cleaned_data['content'])
                messages.success(request, 'Tip created successfully!')
                return redirect('create')
            except Exception as e:
                form.add_error('content', str(e))

    else:
        form = TipForm()
    return render(request, 'create_tip.html', {'form': form, "connected": request.user.is_authenticated})

def list_tips(request):
    tips = Tip.objects.all().order_by("date")
    print("la", tips)
    return render(request, 'list_tips.html', {'tips': tips, "connected": request.user.is_authenticated})

@login_required(login_url='login')
def delete_tip(request, tip_id):
    tip = Tip.objects.get(id=tip_id)
    if tip.author == request.user or request.user.has_perm("ex.delete_tip"):
        if request.method == "POST":
            Tip.objects.get(id=tip_id).delete()
    else:
        messages.error(request, 'You do not have permission to delete this tip!')
    return redirect('list')
#---------vote--------------------------

@login_required(login_url='login')
def upvote(request, tip_id):
    if request.method == 'POST':
        tip = Tip.objects.get(id=tip_id)
        user = tip.author
        if tip.upvotes.filter(id=request.user.id).exists():
            tip.upvotes.remove(request.user.id)
            user.reputation -= 5
        elif tip.downvotes.filter(id=request.user.id).exists():
            tip.downvotes.remove(request.user.id)
            tip.upvotes.add(request.user.id)
            user.reputation += 7
        else:
            tip.upvotes.add(request.user.id)
            user.reputation += 5
        tip.save()
        user.save()
    return redirect('list')

@login_required(login_url='login')
def downvote(request, tip_id):
    tip = Tip.objects.get(id=tip_id)
    if (not request.user.has_perm("ex.can_downvote")) and request.user.username != tip.author.username:
        messages.error(request, 'You do not have permission to downvote this tip!')
        return redirect('list')
    if request.method == 'POST':
        tip = Tip.objects.get(id=tip_id)
        user = tip.author
        if tip.downvotes.filter(id=request.user.id).exists():
            tip.downvotes.remove(request.user.id)
            user.reputation += 2
        elif tip.upvotes.filter(id=request.user.id).exists():
            tip.upvotes.remove(request.user.id)
            tip.downvotes.add(request.user.id)
            user.reputation -= 7
        else:
            tip.downvotes.add(request.user.id)
            user.reputation -= 2
        tip.save()
        user.save()
    return redirect('list')