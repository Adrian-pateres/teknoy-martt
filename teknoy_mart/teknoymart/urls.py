from django.urls import path, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    # --- Product CRUD ---
    path("products/", views.product_list, name="product_list"),                      # READ
    path("products/add/", views.add_product, name="add_product"),                    # CREATE
    path("products/<int:pk>/edit/", views.edit_product, name="edit_product"),        # UPDATE
    path("products/<int:pk>/delete/", views.delete_product, name="delete_product"),  # DELETE


    path("home/", views.home, name="home"),                    # seller dashboard
    path("home-buyer/", views.buyer_home, name="home_buyer"),  # buyer dashboard    
    
    # Landing / Home
    path("", views.index, name="index"),
    path("guest/", views.guest_home, name="guest_home"),
    
    # Dashboards
    path("home/", views.home, name="home"),                  # seller dashboard


    # Authentication
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Registration Wizard
    path("register/", views.register_step1, name="register_step1"),
    path("register/step2/", views.register_step2, name="register_step2"),
    path("register/step3/", views.register_step3, name="register_step3"),
    path("register/step4/", views.register_step4, name="register_step4"),
    path("add-product/", views.add_product, name="add_product"),
    path('myproducts/', views.product_list, name='product_list'),
    
    # --- About Page ---
    path("about/", views.about, name="about"),

    # --- Settings Pages ---
    path("settings/preferences/", views.preferences_view, name="preferences"),
    path("settings/privacy/", views.privacy_settings_view, name="privacy_settings"),
    path("settings/terms/", views.terms_view, name="terms"),
    path("settings/about/", views.settings_about_view, name="settings_about"),

    # Product Upload
    path("products/new/", views.add_product, name="add_product"),  # unified

    # -------- Password Reset Flow --------
    path(
        "forgot-password/",
        auth_views.PasswordResetView.as_view(
            template_name="password/forgot_password.html",
            email_template_name="emails/password_reset_email.txt",
            subject_template_name="emails/password_reset_subject.txt",
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

    # Buyer purchase
    path("buy-now/<int:product_id>/", views.buy_now, name="buy_now"),
    path("payment-success/", views.payment_success, name="payment_success"),
    
    # --- Buyer Settings Pages ---
    path("buyer/settings/preferences/", views.buyer_preferences_view, name="buyer_preferences"),
    path("buyer/settings/privacy/", views.buyer_privacy_view, name="buyer_privacy_settings"),
    path("buyer/settings/terms/", views.buyer_terms_view, name="buyer_terms"),

    # SELLER Delete
    path("settings/delete-account/", views.delete_account_view, name="delete_account"),

    # BUYER Delete
    path("buyer/settings/delete-account/", views.buyer_delete_account_view, name="buyer_delete_account"),

    path("profile/", views.profile_view, name="profile"),
    
    path("password-change/", auth_views.PasswordChangeView.as_view(template_name="password/change_password.html", success_url="/profile/"), name="change_password"),

    path("logout-confirm/", views.logout_page_view, name="logout_confirm"),
    path("logout/", views.logout_view, name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
