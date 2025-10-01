from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .validators import validate_institutional_email

COURSE_CHOICES = [
    ("BSCS", "BS Computer Science"),
    ("BSIT", "BS Information Technology"),
    ("BSECE", "BS Electronics Engineering"),
    ("BSCE", "BS Civil Engineering"),
    ("BSEE", "BS Electrical Engineering"),
    ("BSME", "BS Mechanical Engineering"),
    ("BSArch", "BS Architecture"),
    ("BSBA", "BS Business Administration"),
    ("BSA", "BS Accountancy"),
    ("BSED", "BS Education"),
    ("BSPsych", "BS Psychology"),
    ("BSPolSci", "BS Political Science"),
]

class StudentRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=150)
    full_name  = forms.CharField(max_length=150)
    email      = forms.EmailField(validators=[validate_institutional_email])
    student_id = forms.CharField(max_length=32)
    course     = forms.ChoiceField(choices=[("", "-- Select Course --"), *COURSE_CHOICES])
    password   = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean(self):
        data = super().clean()
        p1 = data.get("password")
        p2 = data.get("confirm_password")
        if p1 and p2 and p1 != p2:
            self.add_error("confirm_password", "Passwords do not match.")
        return data

    def save(self):
        """Create the Django auth user. Use student_id as username."""
        user = User.objects.create_user(
            username=self.cleaned_data["student_id"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["full_name"],
        )
        return user
