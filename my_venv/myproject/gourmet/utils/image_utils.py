from PIL import Image
import io
from django.core.files.base import ContentFile

def save_compressed_image(original_image, original_filename):
    # 圧縮処理
    image = Image.open(original_image)
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG', quality=85)  # 例としてJPEG形式に圧縮
    buffer.seek(0)  # バッファの先頭にシーク

    # 新しいファイル名を設定
    new_filename = f"{original_filename}_compressed.jpg"
    new_image = ContentFile(buffer.read(), name=new_filename)
    return new_image