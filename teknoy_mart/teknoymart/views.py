from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import StudentRegistrationForm, ProductForm
from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Product, Profile
from django.http import HttpResponseForbidden

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

# -------- Role-based decorator --------
def role_required(required):  # use: @role_required("seller") or @role_required("buyer")
    def decorator(view_fn):
        @login_required(login_url="login")
        def _wrapped(request, *args, **kwargs):
            try:
                role = request.user.profile.role
            except Profile.DoesNotExist:
                return HttpResponseForbidden("Profile not found.")
            if role != required:
                return HttpResponseForbidden("You do not have access to this page.")
            return view_fn(request, *args, **kwargs)
        return _wrapped
    return decorator

# ---------------- Landing / Home ----------------
def index(request):
    return render(request, "teknoymart/index.html")

def about(request):
    return render(request, "teknoymart/about.html")

def guest_home(request):
    return render(request, "home/guest_home.html")

@login_required(login_url='guest_home')
@role_required("seller")
def home(request):
    products = Product.objects.filter(owner=request.user).order_by("-created_at")
    return render(request, "home/home.html", {"products": products})

@login_required(login_url='guest_home')
@role_required("buyer")
def home_buyer(request):
    products = Product.objects.all().order_by("-created_at")
    return render(request, "home/home_buyer.html", {"products": products})

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
            return render(request, 'register/register.html')

        if not first or not last:
            messages.error(request, "First name and Last name are required.")
            return render(request, 'register/register.html')

        request.session['first_name'] = first
        request.session['middle_name'] = middle
        request.session['last_name'] = last
        request.session['email'] = email
        request.session['dob'] = request.POST.get('dob', '')

        return redirect('register_step2')

    return render(request, 'register/register.html')

def register_step2(request):
    if request.method == 'POST':
        email = (request.POST.get('email') or request.session.get('email') or '').strip()
        username = (request.POST.get('username') or request.POST.get('student_id') or '').strip()
        pwd1 = request.POST.get('password') or ''
        pwd2 = request.POST.get('confirm_password') or ''

        if not email:
            messages.error(request, "Email is required.")
            return render(request, 'register/register2.html')
        em = email.lower()
        if '@' not in em or em.split('@',1)[1] not in ('cit.edu', 'cit.edu.ph'):
            messages.error(request, "Please use institutional email (@cit.edu or @cit.edu.ph).")
            return render(request, 'register/register2.html')

        if not username:
            messages.error(request, "Student ID is required.")
            return render(request, 'register/register2.html')

        if pwd1 != pwd2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register/register2.html')

        request.session['email'] = email
        request.session['username'] = username
        request.session['password'] = pwd1

        return redirect('register_step3')

    return render(request, 'register/register2.html')

def register_step3(request):
    if request.method == 'POST':
        role = request.POST.get('user_type', '').strip()
        if role not in ('seller', 'buyer'):
            messages.error(request, "Please choose either Seller or Buyer.")
            return render(request, 'register/register3.html')
        request.session['role'] = role
        return redirect('register_step4')

    return render(request, 'register/register3.html')

def register_step4(request):
    needed = ['first_name', 'last_name', 'email', 'username', 'password', 'role']
    if any(not request.session.get(k) for k in needed):
        messages.error(request, "Your session expired. Please start registration again.")
        return redirect('register_step1')

    if request.method == 'POST':
        first_name = request.session['first_name']
        last_name  = request.session['last_name']
        email      = request.session['email']
        username   = request.session['username']
        password   = request.session['password']
        role       = request.session['role']

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
        )
        Profile.objects.create(user=user, role=role)

        # Clear session keys
        for k in ("first_name","middle_name","last_name","email","dob","username","password","confirm_password","role"):
            request.session.pop(k, None)

        messages.success(request, "Registration successful! You can now log in.")
        return redirect('login')

    return render(request, 'register/register4.html')

# ---------------- Authentication ----------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            role = getattr(getattr(user, "profile", None), "role", None)
            if role == "seller":
                return redirect("home")
            elif role == "buyer":
                return redirect("home_buyer")
            else:
                messages.warning(request, "No role found; redirecting to guest page.")
                return redirect("guest_home")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "login/login.html")

def logout_view(request):
    logout(request)
    return redirect("index")

# ---------------- Product Views ----------------
@login_required
@role_required("seller")
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            messages.success(request, "Product added successfully.")
            return redirect("product_list")
        messages.error(request, "Please correct the errors below.")
    else:
        form = ProductForm()
    return render(request, "product/add_product.html", {"form": form, "editing": False})

@login_required
@role_required("seller")
def product_list(request):
    products = Product.objects.filter(owner=request.user).order_by("-created_at")
    return render(request, "product/product_list.html", {"products": products})

@login_required
@role_required("seller")
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, owner=request.user)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect("product_list")
        messages.error(request, "Please correct the errors below.")
    else:
        form = ProductForm(instance=product)
    return render(request, "product/add_product.html", {"form": form, "editing": True, "product": product})

@login_required
@role_required("seller")
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, owner=request.user)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully.")
    return redirect("product_list")


@login_required
@role_required("buyer")
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        payment_method = request.POST.get("payment_method")
        ref_number = request.POST.get("reference_number")

        if not payment_method:
            messages.error(request, "Please select a payment method.")
            return redirect("buy_now", product_id=product.id)

        if not ref_number or len(ref_number.strip()) < 6:
            messages.error(request, "Please enter a valid reference number.")
            return redirect("buy_now", product_id=product.id)

        # TODO: You can save transaction record here later
        messages.success(request, "Payment successful!")
        return redirect("payment_success")

    return render(request, "home/buy_now.html", {"product": product})


@login_required
@role_required("buyer")
def payment_success(request):
    return render(request, "home/payment_success.html")