from django.urls import path, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    # --- Landing / Home ---
    path("", views.index, name="index"),                # Home page
    path("guest/", views.guest_home, name="guest_home"),

    # --- Dashboards ---
    path("home/", views.home, name="home"),            # seller dashboard
    path("home/buyer/", views.home_buyer, name="home_buyer"),  # buyer dashboard

    # --- Product CRUD ---
    path("products/", views.product_list, name="product_list"),                      # READ
    path("products/add/", views.add_product, name="add_product"),                    # CREATE
    path("products/<int:pk>/edit/", views.edit_product, name="edit_product"),        # UPDATE
    path("products/<int:pk>/delete/", views.delete_product, name="delete_product"),  # DELETE

    # --- User Authentication ---
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # --- Registration Wizard ---
    path("register/", views.register_step1, name="register_step1"),
    path("register/step2/", views.register_step2, name="register_step2"),
    path("register/step3/", views.register_step3, name="register_step3"),
    path("register/step4/", views.register_step4, name="register_step4"),

    # --- About Page ---
    path("about/", views.about, name="about"),

    # --- Password Reset Flow ---
    path(
        "forgot-password/",
        auth_views.PasswordResetView.as_view(
            template_name="password/forgot_password.html",
            success_url=reverse_lazy("password_reset_done"),
        ),
        name="forgot_password",
    ),
    path(
        "forgot-password/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="reset_password.html",
            success_url=reverse_lazy("password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),

        path("buy-now/<int:product_id>/", views.buy_now, name="buy_now"),
    path("payment-success/", views.payment_success, name="payment_success"),
]

# --- Static & Media Files ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
