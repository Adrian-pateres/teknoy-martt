from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import StudentRegistrationForm
from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError


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


def register_step1(request):
    if request.method == 'POST':
        request.session['first_name'] = request.POST.get('first_name')
        request.session['middle_name'] = request.POST.get('middle_name')
        request.session['last_name'] = request.POST.get('last_name')
        request.session['dob'] = request.POST.get('dob')
        return redirect('register_step2')  # ✅ should go to step 2
    return render(request, 'register.html')


def register_step2(request):
    if request.method == 'POST':
        request.session['email'] = request.POST.get('email')
        request.session['password'] = request.POST.get('password')
        request.session['confirm_password'] = request.POST.get('confirm_password')
        return redirect('register_step3')  # ✅ next is step 3
    return render(request, 'register2.html')


def register_step3(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        # Save or process user info here if needed
        return redirect('home')
    return render(request, 'register3.html')

def register_step4(request):
    return render(request, "register4.html")

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
