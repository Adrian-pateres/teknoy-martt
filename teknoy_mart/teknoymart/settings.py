# --- Email Configuration (Gmail) ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'adpateres@gmail.com'  # <--- REPLACE WITH YOUR GMAIL
EMAIL_HOST_PASSWORD = 'azec bfet rtcn djuw' # <--- REPLACE WITH YOUR APP PASSWORD

# --- CLOUDINARY CONFIGURATION (For Image Storage) ---
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Replace these with your actual values from the Cloudinary Dashboard
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dppguhfp8',
    'API_KEY': '447487762999893',
    'API_SECRET': 'MROUTRArTbig8QTolY7txQI7P5k',
}

# Tell Django to use Cloudinary for media files (uploaded images)
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Static files (CSS/JS) can still live on Render (using Whitenoise if you have it), 
# but MEDIA files (images) go to Cloudinary.
MEDIA_URL = '/media/'