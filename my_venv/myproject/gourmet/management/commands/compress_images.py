from PIL import Image, ImageOps
from django.core.files import File
from django.core.management.base import BaseCommand
from django.conf import settings
import os
from gourmet.models import StoreInfo  # モデルのインポート

class Command(BaseCommand):
    help = 'メディアディレクトリ内の画像を全て85%に圧縮し、photo1、photo2、photo3 フィールドに上書き保存'

    def handle(self, *args, **kwargs):
        media_root = settings.MEDIA_ROOT
        for root, dirs, files in os.walk(media_root):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    file_path = os.path.join(root, file)
                    # 圧縮画像で元の画像フィールドを上書きする
                    self.compress_images(file_path)

    def compress_images(self, file_path):
        # 圧縮済みのマーカーを付けた新しいファイルパスを作成
        if '_compressed' in os.path.basename(file_path):
            # 圧縮済みのファイルはスキップ
            self.stdout.write(self.style.SUCCESS(f'Skipping already compressed file {file_path}'))
            return
        
        compressed_file_path = f"{os.path.splitext(file_path)[0]}_compressed{os.path.splitext(file_path)[1]}"
        
        try:
            with Image.open(file_path) as img:
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                img = ImageOps.exif_transpose(img)  # Exifデータに基づいて画像を回転
                img.save(compressed_file_path, optimize=True, quality=85)
            
            # 圧縮画像で元の画像フィールドを上書き
            with open(compressed_file_path, 'rb') as f:
                django_file = File(f, name=os.path.basename(compressed_file_path))
                
                for storeinfo in StoreInfo.objects.all():
                    if storeinfo.photo1.name == os.path.basename(file_path):
                        storeinfo.photo1.delete(save=False)  # 古いファイルを削除
                        storeinfo.photo1.save(django_file.name, django_file, save=True)
                    elif storeinfo.photo2.name == os.path.basename(file_path):
                        storeinfo.photo2.delete(save=False)  # 古いファイルを削除
                        storeinfo.photo2.save(django_file.name, django_file, save=True)
                    elif storeinfo.photo3.name == os.path.basename(file_path):
                        storeinfo.photo3.delete(save=False)  # 古いファイルを削除
                        storeinfo.photo3.save(django_file.name, django_file, save=True)
            
            self.stdout.write(self.style.SUCCESS(f'Compressed and saved as {compressed_file_path}'))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error processing {file_path}: {str(e)}'))