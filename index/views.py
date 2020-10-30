from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db import IntegrityError
from .models import User, Model
import secrets
import json

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    else:
        models = Model.objects.filter(owner = request.user)
        return render(request, "index/index.html", {
            "models": models
            })

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

def create(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    else:
        if request.method == "POST":
            name = request.POST["target-name"]
            code = secrets.token_hex(50)
            model = Model(owner = request.user, password = code, name=name)
            model.save()
            return HttpResponseRedirect(reverse('index'))

def delete(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    else:
        if request.method == "POST":
            data = json.loads(request.body)
            passcode = data["passcode"]
            model = Model.objects.get(password = passcode)
            model.delete()
            return JsonResponse({"message": "Success"})