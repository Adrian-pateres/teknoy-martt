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


def register(request):
    if request.method == "POST":
        # pull values exactly as your template sends them
        first_name = request.POST.get("first_name", "").strip()
        last_name  = (request.POST.get("full_name") or request.POST.get("last_name") or "").strip()
        email      = (request.POST.get("email") or "").strip().lower()
        student_id = request.POST.get("student_id", "").strip()  # saved as username
        course     = request.POST.get("course", "").strip()      # not stored in auth_user (OK)
        password   = request.POST.get("password") or ""
        confirm    = request.POST.get("confirm_password") or ""

        # basic server-side checks (match your front-end)
        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return render(request, "register.html", {"form": request.POST})

        if not (email.endswith("@cit.edu") or email.endswith("@cit.edu.ph")):
            messages.error(request, "Please use institutional email.")
            return render(request, "register.html", {"form": request.POST})

        if not first_name or not last_name or not student_id or not course:
            messages.error(request, "Please complete all required fields.")
            return render(request, "register.html", {"form": request.POST})

        try:
            user = User.objects.create_user(
                username=student_id,         # Student ID shows in auth_user.username
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
        except IntegrityError:
            messages.error(request, "That Student ID or email is already registered.")
            return render(request, "register.html", {"form": request.POST})

        login(request, user)
        return redirect("home")

    # GET
    return render(request, "register.html", {"form": StudentRegistrationForm()})

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
