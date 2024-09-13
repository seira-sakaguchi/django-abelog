from PIL import Image, ImageOps
from django.core.files import File
from django.core.management.base import BaseCommand
from django.conf import settings
import os
from gourmet.models import StoreInfo,Mypage,Review

class Command(BaseCommand):
    help = 'メディアディレクトリ内の画像を全て85%に圧縮し、photo1_compressed、photo2_compressed、photo3_compressed フィールドに上書き保存'

    def handle(self, *args, **kwargs):
        media_root = settings.MEDIA_ROOT
        for root, dirs, files in os.walk(media_root):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    file_path = os.path.join(root, file)
                    self.compress_images(file_path)

    def compress_images(self, file_path):
        if '_compressed' in os.path.basename(file_path):
            self.stdout.write(self.style.SUCCESS(f'Skipping already compressed file {file_path}'))
            return

        compressed_file_path = f"{os.path.splitext(file_path)[0]}_compressed{os.path.splitext(file_path)[1]}"
        
        try:
            with Image.open(file_path) as img:
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                img = ImageOps.exif_transpose(img)  # Exifデータに基づいて画像を回転
                img.save(compressed_file_path, optimize=True, quality=85)
            
            with open(compressed_file_path, 'rb') as f:
                django_file = File(f, name=os.path.basename(compressed_file_path))
                
                for storeinfo in StoreInfo.objects.all():
                    if storeinfo.photo1.name == os.path.basename(file_path):
                        storeinfo.photo1_compressed.delete(save=False)
                        storeinfo.photo1_compressed.save(django_file.name, django_file, save=True)
                    elif storeinfo.photo2.name == os.path.basename(file_path):
                        storeinfo.photo2_compressed.delete(save=False)
                        storeinfo.photo2_compressed.save(django_file.name, django_file, save=True)
                    elif storeinfo.photo3.name == os.path.basename(file_path):
                        storeinfo.photo3_compressed.delete(save=False)
                        storeinfo.photo3_compressed.save(django_file.name, django_file, save=True)


                for mypage in Mypage.objects.all():
                    if mypage.photo1.name == os.path.basename(file_path):
                        mypage.photo1_mycompressed.delete(save=False)
                        mypage.photo1_mycompressed.save(django_file.name, django_file, save=True)
                    elif mypage.photo2.name == os.path.basename(file_path):
                        mypage.photo2_mycompressed.delete(save=False)
                        mypage.photo2_mycompressed.save(django_file.name, django_file, save=True)
                    elif mypage.photo3.name == os.path.basename(file_path):
                        mypage.photo3_mycompressed.delete(save=False)
                        mypage.photo3_mycompressed.save(django_file.name, django_file, save=True)
                        
                self.stdout.write(f"Review photo: {review.review_photo1.name}, File: {os.path.basename(file_path)}")
                for review in Review.objects.all():
                    if review.review_photo1.name == os.path.basename(file_path):
                        review.photo1_compressed.delete(save=False)
                        review.photo1_compressed.save(django_file.name, django_file, save=True)
                    elif review.review_photo2.name == os.path.basename(file_path):
                        review.photo2_compressed.delete(save=False)
                        review.photo2_compressed.save(django_file.name, django_file, save=True)
                    elif review.review_photo3.name == os.path.basename(file_path):
                        review.photo3_compressed.delete(save=False)
                        review.photo3_compressed.save(django_file.name, django_file, save=True)
            
            self.stdout.write(self.style.SUCCESS(f'Compressed and saved as {compressed_file_path}'))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error processing {file_path}: {str(e)}'))