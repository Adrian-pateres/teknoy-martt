from django.core.exceptions import ValidationError

ALLOWED_EMAIL_DOMAINS = {"cit.edu", "cit.edu.ph"}

def validate_institutional_email(value: str):
    email = (value or "").strip().lower()
    if "@" not in email:
        raise ValidationError("Enter a valid email address.")
    domain = email.split("@", 1)[1]
    if domain not in ALLOWED_EMAIL_DOMAINS:
        allowed = ", ".join(sorted(ALLOWED_EMAIL_DOMAINS))
        raise ValidationError(f"Use your institutional email ({allowed}).")