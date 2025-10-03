from django.core.exceptions import ValidationError

ALLOWED_EMAIL_DOMAINS = {"cit.edu", "cit.edu.ph"}

def validate_institutional_email(value: str):
    v = (value or "").strip().lower()
    if "@" not in v:
        return
    domain = v.split("@", 1)[1]
    if domain not in ALLOWED_EMAIL_DOMAINS:
        raise ValidationError("Must be an institutional email (@cit.edu or @cit.edu.ph).")