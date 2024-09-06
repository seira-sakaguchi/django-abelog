import os
from django.conf import settings

def delete_compressed_images():
    media_root = settings.MEDIA_ROOT
    for root, dirs, files in os.walk(media_root):
        for file in files:
            if '_compressed' in file.lower():
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Deleted {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {str(e)}")

if __name__ == "__main__":
    delete_compressed_images()