from django.db import models
from django.db.models import UniqueConstraint
from accounts.models import CustomUser

from django.contrib.auth import get_user_model

CustomUser = get_user_model()

# カテゴリ分類(Productクラスより上で定義する必要がある。)
class Category(models.Model):
    # categoryはプルダウン式のため、選択肢を記載(管理画面からはカテゴリを新規登録できない仕様にしている。)

    category_choices = [
    ('和食', '和食'),
    ('中華', '中華'),
    ('イタリアン', 'イタリアン'),
    ('フレンチ', 'フレンチ'),
    ('寿司','寿司'),
    ('焼肉','焼肉'),
    ('韓国料理','韓国料理'),
    ('タイ料理','タイ料理'),
    ('スペイン料理','スペイン料理')
]

    category = models.CharField(verbose_name='ジャンル', choices=category_choices, max_length=50)
    
    def __str__(self):
        return dict(self.category_choices)[self.category]

#店舗詳細
class StoreInfo(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー',on_delete=models.PROTECT)
    store_name = models.CharField(verbose_name='店舗名',max_length=40)
    #カテゴリーはForeignKey
    category = models.ForeignKey(Category,verbose_name='ジャンル', on_delete=models.PROTECT)
    store_detail = models.TextField(verbose_name='店舗詳細',blank=True, null=True)
    photo1 = models.ImageField(verbose_name='写真1',blank=True,default='noImage.png')
    photo2 = models.ImageField(verbose_name='写真2',blank=True,default='noImage.png')
    photo3 = models.ImageField(verbose_name='写真3',blank=True,default='noImage.png')
    create_at = models.DateTimeField(verbose_name='作成日時',auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時',auto_now=True)

    class Meta:
        verbose_name_plural = 'StoreInfo'

    def __str__(self):
        return self.store_name
    
#予約情報
class Reservation(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー',on_delete=models.PROTECT)
    store_name = models.ForeignKey(StoreInfo, verbose_name='店名',on_delete=models.PROTECT)
    date = models.DateField(verbose_name='予約日')
    time = models.TimeField(verbose_name='予約時間')
    persons = models.IntegerField(verbose_name='予約人数')

#レビュー
class Review(models.Model):
    score = models.PositiveIntegerField(blank=False, default=1)
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー',on_delete=models.CASCADE, null=True)
    store_name = models.ForeignKey(StoreInfo, verbose_name='店名',on_delete=models.PROTECT)
    handle = models.CharField(verbose_name='ニックネーム',max_length=50)
    title = models.CharField(verbose_name='タイトル',max_length=50)
    content = models.TextField(verbose_name='レビュー内容')
    create_at = models.DateTimeField(verbose_name='作成日時',auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時',auto_now=True)

    def __str__(self):
        return self.user.username
    
#お気に入り機能
class Like(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー',on_delete=models.PROTECT)
    fav = models.ForeignKey(StoreInfo, verbose_name='お気に入り店舗', on_delete=models.CASCADE) #StoreInfoクラスの各インスタンスを識別するための変数
    create_at = models.DateTimeField(auto_now_add=True)

    #userとfavの組み合わせが一意=同じユーザーが同じレビューに対して複数回いいねすることができないようにDBレベルで制約をつける。
    class Meta:
        constraints = [
            UniqueConstraint(fields=['user','fav'], name='unique_user_fav')
        ]
    def __str__(self):
        return f"{self.user.username}が{self.fav.store_name}をいいねしました"
        # return self.fav.store_name