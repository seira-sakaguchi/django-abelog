from PIL import Image, ImageOps
from django.core.management.base import BaseCommand
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'メディアディレクトリ内の画像を全部85%に圧縮'

    def handle(self, *args, **kwargs):
        media_root = settings.MEDIA_ROOT
        for root, dirs, files in os.walk(media_root):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    file_path = os.path.join(root, file)
                    # チェックしてから圧縮
                    if not self.is_compressed(file_path):
                        self.compress_image(file_path)
                    else:
                        self.stdout.write(self.style.SUCCESS(f'Already compressed {file_path}'))

    def is_compressed(self, file_path):
        # ファイル名に '_compressed' が含まれている場合は圧縮済み
        return '_compressed' in file_path

    def compress_image(self, file_path):
        # 圧縮済みのマーカーを付けた新しいファイルパスを作成
        compressed_file_path = f"{os.path.splitext(file_path)[0]}_compressed{os.path.splitext(file_path)[1]}"
        
        try:
            with Image.open(file_path) as img:
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                img = ImageOps.exif_transpose(img)  # Exifデータに基づいて画像を回転
                img.save(compressed_file_path, optimize=True, quality=85)
                self.stdout.write(self.style.SUCCESS(f'Compressed and saved as {compressed_file_path}'))
        
            # 元のファイルを削除する場合は以下の行のコメントを解除
            # os.remove(file_path)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error processing {file_path}: {str(e)}'))