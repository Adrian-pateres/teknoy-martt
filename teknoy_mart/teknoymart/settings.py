
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'adpateres@gmail.com'
EMAIL_HOST_PASSWORD = 'azec bfet rtcn djuw'



import cloudinary
import cloudinary.uploader
import cloudinary.api


CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dppguhfp8',
    'API_KEY': '447487762999893',
    'API_SECRET': 'MROUTRArTbig8QTolY7txQI7P5k',
}


DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


MEDIA_URL = '/media/'