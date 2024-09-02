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
    path('review-edit/<int:pk>/',views.ReviewUpdateView.as_view(),name='review_edit'),
    path('review-delete/<int:pk>/',views.ReviewDeleteView.as_view(),name='review_delete'),
    path('confirm/',views.ConfirmReservation.as_view(),name='confirm'),
    path('like/<int:store_id>',views.toggle_favorite,name='toggle_favorite'), #like_rest(同期処理)からtoggle_favoriteb (非同期処理)に変更
    path('like-list/',views.LikeListView.as_view(),name='like_list'),
    path('toggle-fav/<int:store_id>/', views.toggle_fav,name ='toggle-fav'),
    path('search/',views.SearchResultView.as_view(),name='search'),
    path('member/',views.MemberShipView.as_view(),name='membership'),
    path('only-member/',views.MemberPageView.as_view(),name='membership_page'),
    path('member-update/<int:pk>/',views.MemberUpdateView.as_view(),name='membership_edit'),
    path('membership-delete/<int:pk>/',views.MembershipDeleteView.as_view(),name='membership_delete'),
    path('mypage/',views.MypageListView.as_view(),name='mypage'),
    path('mypage-form/',views.MyPageFormView.as_view(),name='mypage_form'),
    path('mypage-edit/<int:pk>',views.MypageUpdateView.as_view(),name='mypage_edit'),
    path('mypage-delete/<int:pk>',views.MypageDeleteView.as_view(),name='mypage_delete'),
    path('ourpage/',views.OurpageListView.as_view(),name='ourpage'),
    path('want-list/',views.WantView.as_view(),name='want_list'),
    path('want-list-form/',views.WantFormView.as_view(),name='want_list_form'),
    path('want-list-edit/<int:pk>/',views.WantUpdateView.as_view(),name='want_edit'),
    path('want-list-delete/<int:pk>/',views.WantDeleteView.as_view(),name='want_delete'),
]