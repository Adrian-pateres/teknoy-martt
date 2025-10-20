from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import StudentRegistrationForm, ProductForm
from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile

# ---------------- Helper Functions ----------------
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

# ---------------- Index / Home ----------------
def index(request):
    return render(request, "index.html")

def guest_home(request):
    return render(request, "guest_home.html")

@login_required(login_url='guest_home')
def home(request):
    return render(request, "home.html")  # seller dashboard

@login_required(login_url='guest_home')
def home_buyer(request):
    return render(request, "home_buyer.html")  # buyer dashboard

# ---------------- Registration ----------------
def register_step1(request):
    if request.method == 'POST':
        first = request.POST.get('first_name', '').strip()
        middle = request.POST.get('middle_name', '').strip()
        last = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()

        try:
            email = _validate_institutional_email(email)
        except ValidationError as e:
            messages.error(request, str(e))
            return render(request, 'register.html')

        if not first or not last:
            messages.error(request, "First name and Last name are required.")
            return render(request, 'register.html')

        request.session['first_name'] = first
        request.session['middle_name'] = middle
        request.session['last_name'] = last
        request.session['email'] = email
        request.session['dob'] = request.POST.get('dob', '')

        return redirect('register_step2')

    return render(request, 'register.html')

def register_step2(request):
    if request.method == 'POST':
        email = (request.POST.get('email') or request.session.get('email') or '').strip()
        username = (request.POST.get('username') or request.POST.get('student_id') or '').strip()
        pwd1 = request.POST.get('password') or ''
        pwd2 = request.POST.get('confirm_password') or ''

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

        request.session['email'] = email
        request.session['username'] = username
        request.session['password'] = pwd1

        return redirect('register_step3')

    return render(request, 'register2.html')

def register_step3(request):
    if request.method == 'POST':
        role = request.POST.get('user_type', '')
        request.session['user_type'] = role

        first_name = request.session.get('first_name', '')
        last_name  = request.session.get('last_name', '')
        email      = request.session.get('email')
        username   = request.session.get('username')
        password   = request.session.get('password')

        missing = [k for k, v in {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "username": username,
            "password": password,
            "role": role
        }.items() if not v]

        if missing:
            messages.error(request, "Some details are missing. Please restart registration.")
            return redirect('register_step1')

        if User.objects.filter(username=username).exists():
            messages.error(request, "That Student ID is already registered.")
            return redirect('register_step2')
        if User.objects.filter(email=email).exists():
            messages.error(request, "That email is already registered.")
            return redirect('register_step2')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=False,
            is_active=True
        )

        Profile.objects.create(user=user, role=role)
        request.session['registered_user_id'] = user.id

        return redirect('register_step4')

    return render(request, 'register3.html')

def register_step4(request):
    user_id = request.session.get('registered_user_id')
    if not user_id:
        messages.error(request, "Something went wrong. Please restart registration.")
        return redirect('register_step1')

    user = User.objects.get(id=user_id)
    profile = Profile.objects.get(user=user)

    login(request, user)

    for k in ("first_name","middle_name","last_name","email","dob","username","password","user_type","registered_user_id"):
        request.session.pop(k, None)

    messages.success(request, "Account created successfully!")

    return redirect('home') if profile.role == 'seller' else redirect('home_buyer')

# ---------------- Authentication ----------------
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                try:
                    profile = Profile.objects.get(user=user)
                    return redirect('home') if profile.role == 'seller' else redirect('home_buyer')
                except Profile.DoesNotExist:
                    return redirect('home')
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("index")

def forgot_password_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        messages.success(request, f"A password reset link has been sent to {email}.")
        return redirect("login")
    return render(request, "forgot_password.html")

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

# ---------------- Product Views ----------------
@login_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            messages.success(request, "✅ Product added successfully!")
            return redirect("home")
        else:
            messages.error(request, "⚠️ Please correct the errors below.")
    else:
        form = ProductForm()
    return render(request, "product_upload.html", {"form": form})
