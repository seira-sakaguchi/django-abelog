from django.shortcuts import render
from django.views import generic
import os
import stripe
import json
from django.urls import reverse
from django.shortcuts import redirect
from django.http import JsonResponse
from django.http.response import JsonResponse, HttpResponse 
from django.utils.decorators import method_decorator
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from gourmet.models import Stripe_Customer

#stripe決済について参考にしたサイト
#https://note.com/daikinishimatsu/n/n029a7ff01f62



class PaymentIndexView(generic.TemplateView):
    template_name = 'payment_index.html'

    def get_context_data(self, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY

        customer = Stripe_Customer.objects.filter(user = self.request.user).first()
        print(f'{customer}'"←現在のログインユーザー")
        client_reference_id=self.request.user.id
        print(f'{client_reference_id}'"←現在のログインID")
        subscription = stripe.Subscription.retrieve(customer.stripeSubscriptionId)
        print("サブスクリプションのjsonデータ")
        print(subscription)
        product = stripe.Product.retrieve(subscription.plan.product)
        print("activeかどうかを判定",product)

        #htmlに表示
        context = {
            "subscription": subscription,
            "product": product,
        }
        return context

class PaymentSuccessView(generic.TemplateView):
   template_name = "payment_success.html"

class PaymentCancelView(generic.TemplateView):
   template_name = "payment_cancel.html"

def create_checkout_session(request):
   stripe.api_key = 'sk_test_51Q11x3RwNoxwqPY3wi1UPQQlwb0ZYhxsVPwrsIx0p81p0C7g4tcN3rTzxz7RHcuLpRt4ZX1XM2xltTIionkPNHag00b910fCNA'

   try:
       checkout_session = stripe.checkout.Session.create(
           payment_method_types=['card'], #クレカ決済
           line_items=[
                {
                    # Stripeダッシュボードで作成したサブスクリプション用の価格ID
                    'price': 'price_1Q2G28RwNoxwqPY3KG9n4wze',  
                    'quantity': 1,
                },
            ],
           mode='subscription', #月額払いに
           success_url=request.build_absolute_uri(reverse('payment:success')),
           cancel_url=request.build_absolute_uri(reverse('payment:cancel')),
           client_reference_id=request.user.id if request.user.is_authenticated else None, # ここでクライアントリファレンスIDを設定
       )
       return JsonResponse({'id': checkout_session.id})
   except Exception as e:
       print("失敗")
       return JsonResponse({'error':str(e)})    
   
#DjangoでWebhookを受け取るためのビュー
@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body.decode('utf-8')
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':

    #jsondataをフォルダ内に書き込みするテスト  ※webhook使用時   
    # if event['type'] == 'invoice.created':
        # with open("request.json", mode='w') as f:
        #     f.write(str(event))

        session = event['data']['object']

        # Fetch all the required data from session
        client_reference_id = session.get('client_reference_id')
        stripe_customer_id = session.get('customer')
        stripe_subscription_id = session.get('subscription')
        print(client_reference_id)
        print(stripe_customer_id)
        print(stripe_subscription_id)
        # Get the user and create a new Stripe_Customer
 
        user = get_user_model().objects.get(id=client_reference_id)
        print(client_reference_id)
        print(user)
        Stripe_Customer.objects.create(
            user=user,
            stripeCustomerId=stripe_customer_id,
            stripeSubscriptionId=stripe_subscription_id,
        )
        print("usercreate")

        print (' just subscribed.')

    return HttpResponse(status=200)
