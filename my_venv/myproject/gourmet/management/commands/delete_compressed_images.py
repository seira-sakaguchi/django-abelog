from django.core.management.base import BaseCommand
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Delete all compressed images from the media directory'

    def handle(self, *args, **kwargs):
        media_root = settings.MEDIA_ROOT
        for root, dirs, files in os.walk(media_root):
            for file in files:
                if '_compressed' in file.lower():
                    file_path = os.path.join(root, file)
                    try:
                        os.remove(file_path)
                        self.stdout.write(self.style.SUCCESS(f'Deleted {file_path}'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error deleting {file_path}: {str(e)}'))