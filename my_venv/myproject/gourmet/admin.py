from django.contrib import admin

from .models import CustomUser,StoreInfo,Category,Reservation,Review,Like


class StoreInfoAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'category')
    search_fields = ('store_name','category__category')

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user','store_name','date','time','persons')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('store_name','user','handle','title','score')

class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ('email',)

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('category',)



admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(StoreInfo,StoreInfoAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Reservation,ReservationAdmin)
admin.site.register(Review,ReviewAdmin)
admin.site.register(Like)


