from django.db import models

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# カタカナのみを受け付ける正規表現
katakana_regex = RegexValidator(
    r'^[ァ-ヶー]+$',
    'カタカナで入力してください。'
)

# 郵便番号の正規表現（ハイフンなし）
postal_code_regex = RegexValidator(
    regex=r'^\d{7}$',  # 7桁の数字のみを許容する正規表現
    message="郵便番号は7桁の数字で入力してください。",
)

# 電話番号の正規表現（ハイフンありの場合、例: 090-1234-5678）
phone_number_regex = RegexValidator(
    regex=r'^\d{2,4}-\d{2,4}-\d{4}$',  # ハイフン区切りで数字の組み合わせを許容する正規表現
    message="正しい電話番号の形式で入力してください（例: 090-1234-5678）。",
)

class CustomUser(AbstractUser):
    email =models.EmailField(verbose_name='メールアドレス', unique=True, blank=False, null=False, default='') #unique:そのフィールドに保存される値がデータベース内で一意である必要がある(重複を許さない)
    full_name = models.CharField(verbose_name='名前', max_length=30, blank=False, null=False, default='')
    furigana = models.CharField(validators=[katakana_regex], verbose_name='フリガナ*スペースなし', max_length=30, blank=False, null=False, default='')
    handle = models.CharField(verbose_name='ニックネーム',max_length=50,default='',blank=False, null=False)
    postal_code = models.CharField(validators=[postal_code_regex], max_length=7, verbose_name='郵便番号*ハイフンなし', blank=False, null=False, default='') 
    address = models.CharField(verbose_name='住所',max_length=50,blank=False, null=False, default='')
    phone_number = models.CharField(verbose_name='電話番号（例: 090-1234-5678）', max_length=20, validators=[phone_number_regex],blank=False, null=False, default='')

    class Meta:
        verbose_name_plural = 'CustomUser'

