from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import StudentRegistrationForm, ProductForm
from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import ProductForm
from .models import Product 
from .models import Profile
from django.http import HttpResponseForbidden


def role_required(role: str):
    """Require login AND the given profile.role."""
    def decorator(view_func):
        @login_required(login_url="login")
        @user_passes_test(
            lambda u: hasattr(u, "profile") and u.profile.role == role,
            login_url="login"
        )
        def _wrapped(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


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
    return render(request, "teknoymart/index.html")

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
    """
    Step 3: Pick role (seller/buyer).
    Only store the choice in the session and move to Step 4.
    """
    if request.method == 'POST':
        role = request.POST.get('user_type', '').strip()
        if role not in ('seller', 'buyer'):
            messages.error(request, "Please choose either Seller or Buyer.")
            return render(request, 'register3.html')

        # keep only the choice here
        request.session['role'] = role
        return redirect('register_step4')

    return render(request, 'register3.html')

def register_step4(request):
    """
    Step 4:
      - GET  → show the confirmation page with a 'Finish Registration' button
      - POST → create the user + profile, clear session, and send to Login
    """
    # Make sure all required data from steps 1–3 are still present
    needed = ['first_name', 'last_name', 'email', 'username', 'password', 'role']
    if any(not request.session.get(k) for k in needed):
        messages.error(request, "Your session expired. Please start registration again.")
        return redirect('register_step1')

    if request.method == 'POST':
        first_name = request.session['first_name']
        last_name  = request.session['last_name']
        email      = request.session['email']
        username   = request.session['username']  # student ID
        password   = request.session['password']
        role       = request.session['role']

        # duplicates safety
        if User.objects.filter(username=username).exists():
            messages.error(request, "That Student ID is already registered.")
            return redirect('register_step2')
        if User.objects.filter(email=email).exists():
            messages.error(request, "That email is already registered.")
            return redirect('register_step2')

        # create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=False,
            is_active=True,
        )
        Profile.objects.create(user=user, role=role)

        # clear sensitive session data
        for k in ("first_name","middle_name","last_name","email","dob",
                  "username","password","confirm_password","role"):
            request.session.pop(k, None)

        messages.success(request, "")
        return redirect('login')  # ← do NOT log them in here

    # GET: show your confirmation page with a Finish button
    return render(request, 'register4.html')

# ---------------- Authentication ----------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            role = getattr(getattr(user, "profile", None), "role", None)
            # Use our current route names:
            if role == "seller":
                return redirect("home")             # seller dashboard
            elif role == "buyer":
                return redirect("home_buyer")       # buyer dashboard
            else:
                messages.warning(request, "No role on profile; sending to guest.")
                return redirect("guest_home")
        else:
            messages.error(request, "")
    return render(request, "login.html")


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

# -------- Single role decorator --------
def role_required(required):  # use: @role_required("seller") or @role_required("buyer")
    def decorator(view_fn):
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")
            try:
                role = request.user.profile.role  # 'seller' or 'buyer'
            except Profile.DoesNotExist:
                return HttpResponseForbidden("Profile not found.")
            if role != required:
                return HttpResponseForbidden("You do not have access to this page.")
            return view_fn(request, *args, **kwargs)
        return _wrapped
    return decorator


# Sellers can add products
@login_required
@role_required("seller")
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            messages.success(request, "Product added.")
            return redirect("product_list")
        messages.error(request, "Please correct the errors below.")
    else:
        form = ProductForm()
    return render(request, "add_product.html", {"form": form, "editing": False})

# -------- Seller dashboard (named 'home' to match your URLs) --------
@login_required
@role_required("seller")
def home(request):
    # Seller sees only their products
    products = Product.objects.filter(owner=request.user).order_by("-created_at")
    return render(request, "home.html", {"products": products})

# -------- Buyer dashboard --------
@login_required
@role_required("buyer")
def buyer_home(request):
    # Buyer sees all products
    products = Product.objects.all().order_by("-created_at")
    return render(request, "home_buyer.html", {"products": products})

# -------- CRUD: list only MY products (seller) --------
@login_required
@role_required("seller")
def product_list(request):
    products = Product.objects.filter(owner=request.user).order_by("-created_at")
    return render(request, "product_list.html", {"products": products})


# -------- UPDATE --------
@login_required
@role_required("seller")
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, owner=request.user)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated.")
            return redirect("product_list")
        messages.error(request, "Please correct the errors below.")
    else:
        form = ProductForm(instance=product)
    return render(request, "add_product.html", {"form": form, "editing": True, "product": product})


# -------- DELETE --------
@login_required
@role_required("seller")
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, owner=request.user)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted.")
        return redirect("product_list")
    # If someone GETs this URL, just bounce back to list
    return redirect("product_list")


@login_required
@role_required("seller")
def seller_home(request):
    # Show ONLY this seller's products
    products = Product.objects.filter(owner=request.user).order_by("-created_at")
    return render(request, "home.html", {"products": products})


@login_required
@role_required("buyer")
def buyer_home(request):
    # Show marketplace feed for buyers (all products)
    products = Product.objects.all().order_by("-created_at")
    return render(request, "home_buyer.html", {"products": products})
