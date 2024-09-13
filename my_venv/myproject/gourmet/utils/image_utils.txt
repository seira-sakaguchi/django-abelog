from PIL import Image, ImageOps
import io

def compress_image(file):
    # 圧縮処理
    image = Image.open(file)
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG', quality=85)  # 例としてJPEG形式に圧縮

    buffer.seek(0)  # バッファのポインタを先頭に戻す
    return buffer