from django.db import models
from django.db.models import UniqueConstraint
from accounts.models import CustomUser
from django.core.validators import RegexValidator
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect

CustomUser = get_user_model()

import datetime

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
    ('スペイン料理','スペイン料理'),
    ('海鮮','海鮮'),
    ('洋食','洋食'),
    ('バー','バー'),
    ('ハンバーガー','ハンバーガー'),
    ('スイーツ','スイーツ'),
    ('カレー','カレー'),
    ('鉄板焼き/お好み','鉄板焼き/お好み'),
    ('ラーメン','ラーメン'),
    ('ベーカリー','ベーカリー'),
    ('串/揚げ物','串/揚げ物'),
    ('その他','その他')
]

    category = models.CharField(verbose_name='ジャンル', choices=category_choices, max_length=50,null=True,blank=True)
    
    def __str__(self):
        return dict(self.category_choices)[self.category]

#店舗詳細
class StoreInfo(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー',on_delete=models.PROTECT)
    store_name = models.CharField(verbose_name='店舗名',max_length=40)
    #カテゴリーはForeignKey
    category = models.ForeignKey(Category,verbose_name='ジャンル',on_delete=models.CASCADE)
    store_detail = models.TextField(verbose_name='店舗詳細',blank=True, null=True)
    store_address = models.TextField(verbose_name='店舗住所',blank=True,null=True)
    photo1 = models.ImageField(verbose_name='写真1',blank=True,default='noImage.png')
    photo2 = models.ImageField(verbose_name='写真2',blank=True,default='noImage.png')
    photo3 = models.ImageField(verbose_name='写真3',blank=True,default='noImage.png')
    create_at = models.DateTimeField(verbose_name='作成日時',auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時',auto_now=True)

    #定休日追加
    holiday_choices = [
    ('月' ,'月'),
    ('火','火'),
    ('水','水'),
    ('木','木'),
    ('金','金'),
    ('土','土'),
    ('日','日'),
    ('不定休','不定休'),
    ('なし','なし'),
    ('臨時休業','臨時休業')
    ]
    holiday = models.CharField(verbose_name='定休日1',choices=holiday_choices,max_length=10,blank=True,null=True)
    holiday2 = models.CharField(verbose_name='定休日2',choices=holiday_choices,max_length=10,blank=True,null=True)
    holiday3 = models.CharField(verbose_name='定休日3',choices=holiday_choices,max_length=10,blank=True,null=True)


    #不定休の場合は備考記載
    irregular = models.CharField(verbose_name='不定休の場合は備考を記入してください。',max_length=200,blank=True,null=True)

    


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
    review_photo1 = models.ImageField(verbose_name='レビュー写真1',upload_to='reviews/',blank=True)
    review_photo2 = models.ImageField(verbose_name='レビュー写真2',upload_to='reviews/',blank=True)
    review_photo3 = models.ImageField(verbose_name='レビュー写真3',upload_to='reviews/',blank=True)

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

#有料会員リスト

#クレジットカード番号を14~16桁に制限する正規表現
card_regex = RegexValidator(
    regex=r'^\d{14,16}$',  # 7桁の数字のみを許容する正規表現
    message="カード情報が正しくありません。",
)

#大文字のみを許可する正規表現
char_regex = RegexValidator(
    regex = r'^[A-Z\s]+$', #大文字とスペースは許可 
    message="大文字のアルファベットを入力してください。",
)

#カードブランドは追加・削除を容易にするため別で定義
class CardBrand(models.Model):
    name = models.CharField(verbose_name='カードブランド', max_length=50, unique=True)

    def __str__(self):
        return self.name

class Member(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー',on_delete=models.CASCADE, null=False) #ユーザー情報から削除されたらこちらからも削除
    card_brand = models.ForeignKey(CardBrand, on_delete=models.CASCADE)
    last4 = models.CharField(validators=[card_regex],max_length=16) #IntengerFieldを使うと0123が123として保存されてしまうため、文字列として保存してエラーを回避

    MONTH_CHOICES = [('','月')]+[(i, str(i).zfill(2)) for i in range(1, 13)] #zfillで文字列として1桁の数字を0埋め(1,'01')として格納
    exp_month = models.PositiveIntegerField(verbose_name='月',choices=MONTH_CHOICES)

    CURRENT_YEAR = datetime.datetime.now().year
    YEAR_CHOICES = [('','年')]+[(i, str(i)) for i in range(CURRENT_YEAR, CURRENT_YEAR + 20)] #今から20年後までを選択肢として追加
    exp_year = models.PositiveBigIntegerField(verbose_name='年',choices=YEAR_CHOICES)

    cardholder = models.CharField(validators=[char_regex], verbose_name='カード名義',max_length=50,null=True)

    #同じユーザー名で登録を重複しないように制約をつける(複数カード登録も不可)
    class Meta:
        constraints = [
            UniqueConstraint(fields=['user'],name='unique_user_member')
        ]

    def __str__(self):
        return f"{self.user.full_name}さんが有料会員にプランを変更しました。"
    
#マイページ(他ログ)
class Mypage(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー',on_delete=models.CASCADE)
    store_name = models.CharField(verbose_name='お店の名前',max_length=40)
    #カテゴリーはForeignKey
    category = models.ForeignKey(Category,verbose_name='ジャンル',on_delete=models.CASCADE)
    store_address = models.CharField(verbose_name='お店の場所',max_length=40,blank=True,null=True)
    feeling = models.TextField(verbose_name='お店の感想',max_length=70)
    photo1 = models.ImageField(verbose_name='写真1(必須)')
    photo2 = models.ImageField(verbose_name='写真2',blank=True)
    photo3 = models.ImageField(verbose_name='写真3',blank=True)
    create_at = models.DateTimeField(verbose_name='作成日時',auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時',auto_now=True)

    class Meta:
        verbose_name_plural = 'マイページ'

    def __str__(self):
        return self.store_name
