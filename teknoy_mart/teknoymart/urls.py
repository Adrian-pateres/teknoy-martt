from django.urls import path
from . import views
from django.urls import path, reverse_lazy
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("guest/", views.guest_home, name="guest_home"),
    path("home/", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("register/", views.register_step1, name="register_step1"),
    path("register/step2/", views.register_step2, name="register_step2"),
    path("register/step3/", views.register_step3, name="register_step3"),
    path("register/step4/", views.register_step4, name="register_step4"),
    path("add-product/", views.add_product, name="add_product"),
    path('myproducts/', views.product_list, name='product_list'),
    
    

    # -------- Password reset flow (built-in) --------
    # 1) user enters email
    path(
        "forgot-password/",
        auth_views.PasswordResetView.as_view(
            template_name="forgot_password.html",
            success_url=reverse_lazy("password_reset_done"),
        ),
        name="forgot_password",
    ),
    # 2) “we sent you an email” screen
    path(
        "forgot-password/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    # 3) link from email opens this form
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="reset_password.html",
            success_url=reverse_lazy("password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    # 4) finished
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
