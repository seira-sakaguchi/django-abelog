from . import settings_common, settings_dev
from .settings_common import *
 
DEBUG = True
 
ALLOWED_HOSTS = ['abelog1900.com', 'www.abelog1900.com']
 
STATIC_ROOT = '/usr/share/nginx/html/static'
MEDIA_ROOT = '/usr/share/nginx/html/media' #filezillaでアップロードするディレクトリ