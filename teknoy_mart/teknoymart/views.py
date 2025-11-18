from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
<<<<<<< HEAD
from .forms import StudentRegistrationForm, ProductForm, UserPreferencesForm, UserPrivacyForm, TermsAcceptanceForm, ProfileUpdateForm
=======
from .forms import (
    StudentRegistrationForm, 
    ProductForm, 
    UserPreferencesForm, 
    UserPrivacyForm, 
    TermsAcceptanceForm
)
>>>>>>> b05a911db3601e37ff8ac75905f33203cb8184fc
from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
<<<<<<< HEAD
from django.db import IntegrityError
from .forms import ProductForm
from .models import Product, Profile, UserPreferences, UserPrivacySettings
from .models import Profile
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.utils import timezone



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
=======
from .models import Product, Profile, UserPreferences, UserPrivacySettings
from django.http import HttpResponseForbidden
from django.utils import timezone
>>>>>>> b05a911db3601e37ff8ac75905f33203cb8184fc


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

<<<<<<< HEAD
def about(request):
    return render(request, "teknoymart/about.html")

# ---------------- Index / Home ----------------
=======

# -------- Role-based decorator --------
def role_required(required):
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
>>>>>>> b05a911db3601e37ff8ac75905f33203cb8184fc
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
        dob_str = request.session.get('dob')
        Profile.objects.create(user=user, role=role, birth_date=dob_str)

        # Clear session keys
        for k in ("first_name","middle_name","last_name","email","dob","username","password","confirm_password","role"):
            request.session.pop(k, None)

        messages.success(request, "Registration successful! You can now log in.")
<<<<<<< HEAD
        return redirect('login')  # ← do NOT log them in here
=======
        return redirect('login')
>>>>>>> b05a911db3601e37ff8ac75905f33203cb8184fc

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
<<<<<<< HEAD

# -------- Single role decorator --------
def role_required(required):
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
=======
>>>>>>> b05a911db3601e37ff8ac75905f33203cb8184fc
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


<<<<<<< HEAD
# -------- Buyer dashboard --------
@login_required
@role_required("buyer")
def buyer_home(request):
    products = Product.objects.filter(owner__isnull=False).order_by("-created_at")
    return render(request, "home/home_buyer.html", {"products": products})

# -------- CRUD: list only MY products (seller) --------
=======
>>>>>>> b05a911db3601e37ff8ac75905f33203cb8184fc
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
    return render(
        request,
        "product/add_product.html",
        {"form": form, "editing": True, "product": product},
    )


@login_required
@role_required("seller")
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, owner=request.user)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully.")
<<<<<<< HEAD
        return redirect("product_list")
    # If someone GETs this URL, just bounce back to list
=======
>>>>>>> b05a911db3601e37ff8ac75905f33203cb8184fc
    return redirect("product_list")


# --------------- Settings Views ----------------

@login_required(login_url="login")
def preferences_view(request):
    """User preferences page"""
    prefs, _ = UserPreferences.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserPreferencesForm(request.POST, instance=prefs)
        if form.is_valid():
            form.save()
            messages.success(request, "Preferences saved successfully.")
            return redirect("preferences")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserPreferencesForm(instance=prefs)

    return render(request, "settings/preferences.html", {"form": form})


<<<<<<< HEAD
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


# --------------- Settings Views for Seller----------------

@login_required(login_url="login")
def preferences_view(request):
    """User preferences page"""
    prefs, _ = UserPreferences.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserPreferencesForm(request.POST, instance=prefs)
        if form.is_valid():
            form.save()
            messages.success(request, "Preferences saved successfully.")
            return redirect("preferences")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserPreferencesForm(instance=prefs)
        return render(request, "settings-branches/preferences.html", {"form": form})
    

=======
>>>>>>> b05a911db3601e37ff8ac75905f33203cb8184fc
@login_required(login_url="login")
def privacy_settings_view(request):
    """User privacy settings page"""
    settings_obj, _ = UserPrivacySettings.objects.get_or_create(user=request.user)
<<<<<<< HEAD
=======

>>>>>>> b05a911db3601e37ff8ac75905f33203cb8184fc
    if request.method == "POST":
        form = UserPrivacyForm(request.POST, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Privacy settings saved successfully.")
            return redirect("privacy_settings")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserPrivacyForm(instance=settings_obj)
<<<<<<< HEAD
        return render(request, "settings-branches/privacy.html", {"form": form})
    
=======

    return render(request, "settings/privacy.html", {"form": form})

>>>>>>> b05a911db3601e37ff8ac75905f33203cb8184fc

@login_required(login_url="login")
def terms_view(request):
    """Terms & Conditions acceptance page"""
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = TermsAcceptanceForm(request.POST)
        if form.is_valid():
            profile.terms_accepted = True
            profile.terms_accepted_at = timezone.now()
            profile.save()
            messages.success(request, "Thank you for accepting the Terms & Conditions.")
            return redirect("index")
        else:
            messages.error(request, "You must agree to the Terms & Conditions to continue.")
    else:
        initial = {"agree": profile.terms_accepted}
        form = TermsAcceptanceForm(initial=initial)

<<<<<<< HEAD
    return render(request, "settings-branches/terms.html", {"form": form, "profile": profile})
=======
    return render(request, "settings/terms.html", {"form": form, "profile": profile})
>>>>>>> b05a911db3601e37ff8ac75905f33203cb8184fc


@login_required(login_url="login")
def settings_about_view(request):
    """Static informational page about the settings system"""
<<<<<<< HEAD
    return render(request, "settings-branches/about_settings.html")

# ---------------- Buyer Settings Views ----------------

@login_required
@role_required("buyer")
def buyer_preferences_view(request):
    """Buyer specific preferences page"""
    prefs, _ = UserPreferences.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserPreferencesForm(request.POST, instance=prefs)
        if form.is_valid():
            form.save()
            messages.success(request, "Preferences saved successfully.")
            return redirect("buyer_preferences") # Stay on page after save
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserPreferencesForm(instance=prefs)
    
    # This is the key: We load 'buyer_preferences.html' instead of 'preferences.html'
    return render(request, "settings-branches/buyer_preferences.html", {"form": form})


@login_required
@role_required("buyer")
def buyer_privacy_view(request):
    """Buyer specific privacy page"""
    settings_obj, _ = UserPrivacySettings.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        form = UserPrivacyForm(request.POST, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Privacy settings saved successfully.")
            return redirect("buyer_privacy_settings")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserPrivacyForm(instance=settings_obj)
        
    return render(request, "settings-branches/buyer_privacy.html", {"form": form})


@login_required
@role_required("buyer")
def buyer_terms_view(request):
    """Buyer specific terms page"""
    profile, _ = Profile.objects.get_or_create(user=request.user)

    # Note: Usually terms are read-only or just a display for buyers unless you need them to re-accept
    return render(request, "settings-branches/buyer_terms.html", {"profile": profile})


# ---------------- Delete Account Logic ----------------

@login_required(login_url="login")
def delete_account_view(request):
    """
    SELLER: Deletes the account and all associated data (products, profile).
    """
    # 1. If the user clicked "Confirm Delete" (POST request)
    if request.method == "POST":
        user = request.user
        user.delete()  # This permanently deletes the User + Profile + Products
        messages.success(request, "Your account has been successfully deleted.")
        return redirect("index")  # Go back to Landing Page

    # 2. If the user just opened the page (GET request)
    return render(request, "settings-branches/delete_account.html")


@login_required(login_url="login")
def buyer_delete_account_view(request):
    """
    BUYER: Deletes the account and all associated data.
    """
    # 1. If the user clicked "Confirm Delete" (POST request)
    if request.method == "POST":
        user = request.user
        user.delete()  # This permanently deletes the User + Profile
        messages.success(request, "Your account has been successfully deleted.")
        return redirect("index")  # Go back to Landing Page

    # 2. If the user just opened the page (GET request)
    return render(request, "settings-branches/buyer_delete_account.html")


# ---------------- Profile Views ----------------

@login_required
def profile_view(request):
    """
    Unified Profile View. 
    Detects if user is Seller or Buyer and renders the correct template.
    """
    profile, _ = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Update User model (Names)
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.save()

        # Update Profile model (Pic, Bio, DOB)
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)

    context = {
        'form': form,
        'profile': profile,
        'is_seller': profile.role == 'seller'
    }

    # Route to specific templates based on role
    if profile.role == 'seller':
        return render(request, "settings-branches/seller_profile.html", context)
    else:
        return render(request, "settings-branches/buyer_profile.html", context)
    

    # ---------------- Logout Logic ----------------

# 1. This shows the Confirmation Page
@login_required
def logout_page_view(request):
    return render(request, "logout/logout.html")

# 2. This performs the actual logout (triggered by the "Return Home" button)
def logout_view(request):
    logout(request)
    return redirect("index")
=======
    return render(request, "settings/about_settings.html")
>>>>>>> b05a911db3601e37ff8ac75905f33203cb8184fc
