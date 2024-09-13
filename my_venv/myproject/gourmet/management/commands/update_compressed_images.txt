from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from gourmet.models import StoreInfo
from ...utils.image_utils import compress_image

class Command(BaseCommand):
    help = '圧縮画像を保存し、古い画像を削除します。'

    def handle(self, *args, **kwargs):
        for storeinfo in StoreInfo.objects.all():
            self.update_compressed_images(storeinfo)
            self.stdout.write(self.style.SUCCESS(f'Updated images for store: {storeinfo.store_name}'))

    def update_compressed_images(self, storeinfo_instance):
        for field in ['photo1', 'photo2', 'photo3']:
            image_field = getattr(storeinfo_instance, field)
            if not image_field or not image_field.name:
                continue
            if '_compressed' in image_field.name:
                continue
            
            try:
                compressed_image = compress_image(image_field)
            except FileNotFoundError:
                self.stdout.write(self.style.WARNING(f'File not found for {field} in store: {storeinfo_instance.store_name}'))
                continue

            compressed_file = ContentFile(compressed_image.getvalue(), name=f"{image_field.name}_compressed.jpg")

            compressed_field_name = f"{field}_compressed"
            compressed_field = getattr(storeinfo_instance, compressed_field_name)
            compressed_field.save(compressed_file.name, compressed_file, save=True)

            # 古い画像ファイルを削除
            image_field.delete(save=False)