from django.contrib import admin

from .models import CustomUser,StoreInfo,Category,Reservation,Review


class StoreInfoAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'category')
    search_fields = ('store_name',)

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user','store_name','date','time','persons')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('store_name','handle','title')


admin.site.register(CustomUser)
admin.site.register(StoreInfo,StoreInfoAdmin)
admin.site.register(Category)
admin.site.register(Reservation,ReservationAdmin)
admin.site.register(Review,ReviewAdmin)



