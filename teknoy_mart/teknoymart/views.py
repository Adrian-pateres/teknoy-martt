from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import StudentRegistrationForm

def home(request):
    # make sure teknoymart/templates/index.html exists
    return render(request, "index.html")

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