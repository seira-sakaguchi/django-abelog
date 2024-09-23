from django.urls import path
from . import views
from .views import stripe_webhook


app_name = 'payment'
urlpatterns = [
    path('',views.PaymentIndexView.as_view(),name='index'),
    path('create_checkout_session/', views.create_checkout_session, name='checkout_session'),
    path('success/', views.PaymentSuccessView.as_view(), name='success'),
    path('cancel/', views.PaymentCancelView.as_view(), name='cancel'),
    path('webhook/', stripe_webhook, name='webhook'),
]

