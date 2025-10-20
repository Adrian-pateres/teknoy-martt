from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import StudentRegistrationForm
from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import ProductForm
from .models import Product 

def _validate_institutional_email(email: str):
    email = (email or "").strip().lower()
    if not email or "@" not in email:
        raise ValidationError("Please enter a valid email.")
    domain = email.split("@", 1)[1]
    if domain not in ("cit.edu", "cit.edu.ph"):
        raise ValidationError("Please use institutional email (@cit.edu or @cit.edu.ph).")
    return email

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
        first = request.POST.get('first_name', '').strip()
        middle = request.POST.get('middle_name', '').strip()
        last = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()

        # server-side institutional check
        try:
            email = _validate_institutional_email(email)
        except ValidationError as e:
            messages.error(request, str(e))
            return render(request, 'register.html')  # show same step with message

        if not first or not last:
            messages.error(request, "First name and Last name are required.")
            return render(request, 'register.html')

        # store in session
        request.session['first_name'] = first
        request.session['middle_name'] = middle
        request.session['last_name'] = last
        request.session['email'] = email
        # (Optional) if you still collect DOB on this page:
        request.session['dob'] = request.POST.get('dob', '')

        return redirect('register_step2')

    return render(request, 'register.html')


def register_step2(request):
    if request.method == 'POST':
        # email can come from this step OR from step1 session
        email    = (request.POST.get('email') or request.session.get('email') or '').strip()

        # accept either "username" or "student_id" (some templates use student_id)
        username = (request.POST.get('username') or request.POST.get('student_id') or '').strip()

        pwd1     = request.POST.get('password') or ''
        pwd2     = request.POST.get('confirm_password') or ''

        # server-side institutional email guard only if we have an email
        if not email:
            messages.error(request, "Email is required.")
            return render(request, 'register2.html')
        em = email.lower()
        if '@' not in em or em.split('@',1)[1] not in ('cit.edu', 'cit.edu.ph'):
            messages.error(request, "Please use institutional email (@cit.edu or @cit.edu.ph).")
            return render(request, 'register2.html')

        if not username:
            messages.error(request, "Student ID is required.")
            return render(request, 'register2.html')

        if pwd1 != pwd2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register2.html')

        # persist for next step
        request.session['email']    = email
        request.session['username'] = username   # Student ID
        request.session['password'] = pwd1

        return redirect('register_step3')

    return render(request, 'register2.html')


def register_step3(request):
    if request.method == 'POST':
        # optional card selection; not stored in auth_user
        request.session['user_type'] = request.POST.get('user_type', '')

        # gather everything saved across steps
        first_name = request.session.get('first_name') or ''
        last_name  = request.session.get('last_name') or ''
        email      = request.session.get('email')
        username   = request.session.get('username')   # Student ID
        password   = request.session.get('password')

        # ensure required fields exist
        missing = [k for k, v in {
            "first_name": first_name,
            "last_name":  last_name,
            "email":      email,
            "username":   username,
            "password":   password,
        }.items() if not v]
        if missing:
            messages.error(request, "Some details are missing. Please restart registration.")
            return redirect('register_step1')

        # prevent duplicates
        if User.objects.filter(username=username).exists():
            messages.error(request, "")
            return redirect('register_step2')
        if User.objects.filter(email=email).exists():
            messages.error(request, "")
            return redirect('register_step2')

        # CREATE the user (this writes a row to Railway/MySQL immediately)
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=False,   # 0
            is_active=True,   # 1
        )

        # optional: auto-login, then go to your success page
        login(request, user)

        # cleanup wizard data
        for k in ("first_name","middle_name","last_name","dob","email","username","password","user_type"):
            request.session.pop(k, None)

        return redirect('register_step4')  # your success page

    return render(request, 'register3.html')

def register_step4(request):
    # On GET just render the page (you can show a summary using session values)
    if request.method == 'GET':
        return render(request, "register4.html")

    # On POST (click "Finish Registration") create the user
    first = request.session.get('first_name')
    last  = request.session.get('last_name')
    email = request.session.get('email')
    username = request.session.get('username')   # Student ID
    password = request.session.get('password')

    missing = [k for k, v in {
        "first_name": first, "last_name": last, "email": email,
        "username": username, "password": password
    }.items() if not v]
    if missing:
        messages.error(request, "Some details are missing. Please restart registration.")
        return redirect('register_step1')

    # prevent duplicates
    if User.objects.filter(username=username).exists():
        messages.error(request, "That Student ID is already registered.")
        return redirect('register_step2')
    if User.objects.filter(email=email).exists():
        messages.error(request, "That email is already registered.")
        return redirect('register_step1')

    # create & save -> writes row to Railway/Workbench auth_user immediately
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first,
        last_name=last,
        is_staff=False,
        is_active=True,
    )

    # optional: auto-login and go home (your UI shows a “success” page already)
    login(request, user)

    # clear session bits for the wizard
    for k in ("first_name","middle_name","last_name","email","dob","username","password","user_type"):
        request.session.pop(k, None)

    messages.success(request, "Account created!")
    return redirect('home')  # or keep render of register4.html if you prefer

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

# Forgot Password view
def forgot_password_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        # Simulate sending a reset link (you can integrate Django’s PasswordResetView later)
        messages.success(request, f"A password reset link has been sent to {email}.")
        return redirect("login")
    return render(request, "forgot_password.html")

# Reset Password view
def reset_password_view(request):
    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            messages.success(request, "Your password has been successfully reset!")
            return redirect("login")
    return render(request, "reset_password.html")

def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user  # <-- assign the logged-in user
            product.save()
            return redirect('product_list')  # redirect to the product list page
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})


def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'product_list.html', {'products': products})

def home(request):
    # Fetch all products (newest first)
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'products': products})