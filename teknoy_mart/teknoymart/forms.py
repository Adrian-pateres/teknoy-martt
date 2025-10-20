from django import forms
from django.contrib.auth import get_user_model
from .models import Profile, Product
from .validators import validate_institutional_email

class StudentRegistrationForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect,
        required=True,
        label="Register as"
    )

    email = forms.EmailField(
        validators=[validate_institutional_email],
        widget=forms.EmailInput(attrs={
            "id": "email",
            "placeholder": "juan.delacruz@cit.edu",
            "required": "required",
        }),
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={"id": "password"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"id": "confirm_password"}))

    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "username", "email"]  # username = StudentID
        widgets = {
            "first_name": forms.TextInput(attrs={"id": "first_name", "placeholder": "Juan", "required": "required"}),
            "last_name":  forms.TextInput(attrs={"id": "last_name",  "placeholder": "Dela Cruz", "required": "required"}),
            "username":   forms.TextInput(attrs={"id": "student_id", "placeholder": "25-1234-567", "required": "required"}),
        }

    def clean(self):
        cleaned = super().clean()
        pwd = cleaned.get("password")
        cpw = cleaned.get("confirm_password")
        if pwd and cpw and pwd != cpw:
            self.add_error("confirm_password", "Passwords do not match.")
        return cleaned

    def save(self, commit=True):
        # Create the user first
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()
            # Create Profile with selected role
            Profile.objects.create(user=user, role=self.cleaned_data['role'])

        return user


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["title", "price", "category", "description", "image"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "e.g., CIT-U Hoodie"}),
            "price": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "category": forms.Select(),
            "description": forms.Textarea(attrs={"placeholder": "Brief details about your item…"}),
        }
