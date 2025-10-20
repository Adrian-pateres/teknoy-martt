from django import forms
from .models import Product
from django.contrib.auth import get_user_model
from .validators import validate_institutional_email
 
 
class StudentRegistrationForm(forms.ModelForm):
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
        # IMPORTANT: don't bind a model at import time
        model = None
        fields = ["first_name", "last_name", "email", "username"]  # username = StudentID
        widgets = {
            "first_name": forms.TextInput(attrs={"id": "first_name", "placeholder": "Juan", "required": "required"}),
            "last_name":  forms.TextInput(attrs={"id": "last_name",  "placeholder": "Dela Cruz", "required": "required"}),
            "username":   forms.TextInput(attrs={"id": "student_id", "placeholder": "25-1234-567", "required": "required"}),
        }
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Bind the user model only after Django apps are ready
        self._meta.model = get_user_model()
 
    def clean(self):
        cleaned = super().clean()
        pwd = cleaned.get("password")
        cpw = cleaned.get("confirm_password")
        if pwd and cpw and pwd != cpw:
            self.add_error("confirm_password", "Passwords do not match.")
        return cleaned
 
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["title","price","category","description","image"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder":"e.g., CIT-U Hoodie"}),
            "price": forms.NumberInput(attrs={"step":"0.01", "min":"0"}),
            "category": forms.Select(),
            "description": forms.Textarea(attrs={"placeholder":"Brief details about your item…"}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'category', 'price', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter product title', 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'min':0, 'step':0.01, 'class':'form-control'}),
            'description': forms.Textarea(attrs={'placeholder':'Enter product description...', 'class':'form-control'}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and image.size > 2*1024*1024:
            raise forms.ValidationError("Image too large. Max size 2MB.")
        return image