from django.core.files import File
from PIL import Image
import io
from typing import BinaryIO

def save_compressed_image(original_image, original_filename):
    # 圧縮処理
    image = Image.open(original_image)
    buffer = io.BytesIO()
    compressed_filename = f"{original_filename}_compressed.jpg"
    image.save(buffer, format='JPEG', quality=85)  # 例としてJPEG形式に圧縮
    buffer.seek(0)
    new_image = File(buffer, name=compressed_filename)
    return new_image
