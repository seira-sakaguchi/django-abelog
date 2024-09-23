from django.contrib import admin

from .models import CustomUser,StoreInfo,Category,Reservation,Review,Like,Member,CardBrand,Mypage,WantPlace,Stripe_Customer
from import_export import resources
from import_export.admin import ImportExportModelAdmin

#テーブルごとにDBをインポート、エクスポートする(CSVほか)
class StoreInfoResource(resources.ModelResource):
    class Meta:
        model = StoreInfo

class StoreInfoAdmin(ImportExportModelAdmin):
    list_display = ('store_name', 'category')
    search_fields = ('store_name','category__category')
    search_help_text = '店舗名もしくはジャンル検索。'

    resource_class = StoreInfoResource

# チェックボックスで来店済みに変更するアクション
def make_invisible(modeladmin, request, queryset):
    queryset.update(is_visible=True)
make_invisible.short_description = "選択した予約を来店済みにする"


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('is_visible','user','store_name','date','time','persons')
    list_filter = ('is_visible',)

    actions = [make_invisible]  # アクション(操作:)を追加




class ReviewAdmin(admin.ModelAdmin):
    list_display = ('store_name','user','handle','title','score')

class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ('email',)
    search_help_text = 'emailで検索'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category','id')
    search_fields = ('category',)

class MemberAdmin(admin.ModelAdmin):
    list_display = ('id','get_full_name','exp_month','exp_year')

    def get_full_name(self,obj):
        return obj.user.full_name
    get_full_name.short_description = 'フルネーム'


class MypageResource(resources.ModelResource):
    class Meta:
        model = Mypage

class MypageAdmin(ImportExportModelAdmin):
    list_display = ('id','store_name', 'category')
    search_fields = ('store_name','category__category')

    resource_class = MypageResource

class WantPlaceResource(resources.ModelResource):
    class Meta:
        model = WantPlace


class WantPlaceAdmin(ImportExportModelAdmin):
    list_display = ('store_name', 'comment')
    search_fields = ('store_name','comment')
                     
    resource_class = WantPlaceResource

#stripeサブスク会員
class Stripe_CUstomerAdmin(admin.ModelAdmin):
    list_display = ('user','stripeCustomerId', 'regist_date')

admin.site.register(Stripe_Customer,Stripe_CUstomerAdmin)


admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(StoreInfo,StoreInfoAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Reservation,ReservationAdmin)
admin.site.register(Review,ReviewAdmin)
admin.site.register(Like)
admin.site.register(Member,MemberAdmin)
admin.site.register(CardBrand)
admin.site.register(Mypage,MypageAdmin)
admin.site.register(WantPlace,WantPlaceAdmin)

