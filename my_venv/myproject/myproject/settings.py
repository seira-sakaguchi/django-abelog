from . import settings_common, settings_dev
from .settings_common import *
 
DEBUG = True
 
ALLOWED_HOSTS = ['abelog1900.com', 'www.abelog1900.com']

DATA_UPLOAD_MAX_MEMORY_SIZE = 20971520  # 20 MB
 
STATIC_ROOT = '/usr/share/nginx/html/static'
MEDIA_ROOT = '/usr/share/nginx/html/media' #filezillaでアップロードするディレクトリ

EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
EMAIL_HOST_USER = '${ses-smtp-user.20240830-195422}'
EMAIL_HOST_PASSWORD = '${BAB7y1IYf9GF2rkd+L0db39OCRi++HoJNMlzYBli/Aux}'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
