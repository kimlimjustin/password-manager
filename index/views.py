from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db import IntegrityError
from .models import User
import secrets

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request, "index/index.html")

def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        email = request.POST["email"]
        code = secrets.token_hex(10)
        if password != confirmation:
            return render(request, "index/register.html", {
                "message": "Password must match."
            })
        try:
            user = User.objects.create_user(username = username, password = password, code = code, email = email)
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        except IntegrityError:
            return render(request, "index/register.html", {
                "message": "Username already taken."
            })
    else:
        return render(request, "index/register.html")

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "index/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "index/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))