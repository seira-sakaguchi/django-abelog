from django.urls import path
from . import views

app_name = 'gourmet'
urlpatterns = [
    path('',views.TopView.as_view(), name='top'),
    path('detail/<int:pk>',views.StoreDetailView.as_view(),name='detail'),
    path('profile/',views.ProFileView.as_view(),name='profile'),
    path('profile-update/<int:pk>',views.ProfileUpdateView.as_view(),name='profile_update'),
    path('reservation-success/<int:reservation_id>', views.reservation_success, name='reservation_success'),
    path('reserve-list/',views.ReserveListView.as_view(), name='reserve_list'),
    path('reserve-delete/<int:pk>',views.ReserveDeleteView.as_view(),name='reserve_delete'),
    path('review/<int:store_id>/',views.submit_review,name='review_form'),
]