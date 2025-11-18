from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings


class Profile(models.Model):
    ROLE_CHOICES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    # ---- Terms & Conditions tracking ----
    terms_accepted = models.BooleanField(default=False)
    terms_accepted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# --- Existing Supabase User table (not managed by Django) ---
class UserRecord(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.TextField()
    last_name = models.TextField()
    student_id = models.TextField(unique=True)
    course = models.TextField()
    password_hash = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "users"
        managed = False


# --- Product model for sellers ---
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Clothing', 'Clothing'),
        ('Electronics', 'Electronics'),
        ('Food', 'Food'),
        ('Accessories', 'Accessories'),
    ]

    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# ------ Model for user preferences ------
class UserPreferences(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="preferences",
    )
    email_alerts = models.BooleanField(default=True)
    message_notifications = models.BooleanField(default=True)
    system_activity_updates = models.BooleanField(default=False)

    language = models.CharField(
        max_length=10,
        choices=[
            ("en", "English"),
            ("es", "Spanish"),
            ("fr", "French"),
        ],
        default="en",
    )
    time_format_24h = models.BooleanField(default=True)
    homepage_view = models.CharField(
        max_length=20,
        choices=[
            ("dashboard", "Dashboard"),
            ("inbox", "Inbox"),
            ("activity", "Recent Activity"),
        ],
        default="dashboard",
    )

    dark_mode = models.BooleanField(default=False)
    font_size = models.CharField(
        max_length=10,
        choices=[
            ("small", "Small"),
            ("medium", "Medium"),
            ("large", "Large"),
        ],
        default="medium",
    )
    layout_density = models.CharField(
        max_length=10,
        choices=[
            ("comfortable", "Comfortable"),
            ("compact", "Compact"),
        ],
        default="comfortable",
    )

    def __str__(self):
        return f"{self.user} preferences"


# ------ Model for user privacy settings ------
class UserPrivacySettings(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="privacy_settings",
    )

    # Who can see profile/activity
    show_profile_public = models.BooleanField(default=False)
    show_activity_public = models.BooleanField(default=False)

    # Data management flags
    allow_data_export = models.BooleanField(default=True)
    allow_data_analysis = models.BooleanField(default=True)

    # Security related toggles
    two_factor_enabled = models.BooleanField(default=False)
    login_alerts_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user} privacy settings"
