from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import StudentRegistrationForm
from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

# Index (landing page)
def index(request):
    return render(request, "index.html")

# Guest home (view-only)
def guest_home(request):
    return render(request, "guest_home.html")

# Home (dashboard / requires login)
@login_required(login_url='guest_home')
def home(request):
    return render(request, "home.html")


def register(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = StudentRegistrationForm()
    return render(request, "register.html", {"form": form})

# login view
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})

# logout view
def logout_view(request):
    logout(request)
    return redirect("index")  # (landing page) after logout
