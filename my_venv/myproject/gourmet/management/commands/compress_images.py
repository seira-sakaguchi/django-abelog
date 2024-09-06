from django.core.management.base import BaseCommand
from django.conf import settings
import os
from PIL import Image
import io
from ..utils.image_utils import save_compressed_image

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
            with open(file_path, 'rb') as f:
                original_image = f.read()
                original_filename = os.path.splitext(os.path.basename(file_path))[0]
                compressed_image = save_compressed_image(io.BytesIO(original_image), original_filename)
                
                # 圧縮済み画像をディスクに保存
                with open(compressed_file_path, 'wb') as f:
                    f.write(compressed_image.read())
                
                self.stdout.write(self.style.SUCCESS(f'Compressed and saved as {compressed_file_path}'))
        
            # 元のファイルを削除する場合は以下の行のコメントを解除
            # os.remove(file_path)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error processing {file_path}: {str(e)}'))