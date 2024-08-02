from django.contrib import admin

from .models import CustomUser,StoreInfo,Category,Reservation,Review,Like


class StoreInfoAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'category')
    search_fields = ('store_name','category__category')
    search_help_text = '店舗名もしくはジャンル検索。ジャンルを検索する場合は数字で検索してください。(1:和食, 2:中華, 3:イタリアン,  4:フレンチ, 5:寿司, 6:焼肉, 7:韓国料理)'

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user','store_name','date','time','persons')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('store_name','user','handle','title','score')

class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ('email',)
    search_help_text = 'emailで検索'

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('category',)



admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(StoreInfo,StoreInfoAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Reservation,ReservationAdmin)
admin.site.register(Review,ReviewAdmin)
admin.site.register(Like)


