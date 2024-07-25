from django.shortcuts import render,redirect,get_object_or_404
from django.views import generic,View
from django.views.generic import UpdateView, ListView,DeleteView,DetailView
from .models import StoreInfo,Reservation,Review,Like
from accounts.models import CustomUser
from .forms import ProfileForm,ReservationForm,ReviewForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime



#トップページ
class TopView(generic.ListView):
    model = StoreInfo
    template_name = 'top.html'

#店舗詳細ページ
class StoreDetailView(generic.DetailView):
    model = StoreInfo
    template_name = 'store_detail.html'
    print("店名",StoreInfo.store_name)


    def get_context_data(self,**kwargs):
        store = self.get_object()
        context = super().get_context_data(**kwargs)

        #予約フォームの追加
        context['form'] = ReservationForm() #get_context_dataにReservationFormを呼び出す。この'form'という変数をテンプレートで使えるようになる。

        #レビューの取得と追加
        context['reviews'] = Review.objects.filter(store_name=store).order_by('-create_at')

        #ユーザーがお気に入りにしている店舗情報を取得(#全ての'fav'フィールドの値をリストとして取得)
        context['user_likes'] = Like.objects.filter(user=self.request.user).values_list('fav',flat=True) #favはLikeモデルのフィールド名
        '''【解説】
        fileter:userフィールドが現在のリクエストユーザーと一致するLikeオブジェクトを取得。
        values_list:なんで数字のみを取得???'''
        
        return context
    
    #フォームから送信されたデータの処理
    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        form = ReservationForm(request.POST)

        if form.is_valid():
            # print('check',form)
            # print('check',form.data)
            self.request.session['form_date'] = form.data['date']
            self.request.session['form_time'] = form.data['time']
            self.request.session['form_persons'] = form.data['persons']
            self.request.session['form_restaurant'] = pk
            return redirect('gourmet:confirm')
        
        #バリデーションに失敗した場合はフォームとともにテンプレートを再レンダリングする。
        return self.render_to_response(self.get_context_data(form=form))
    
    #レビュー一覧の表示  【**注意!**】上のdef get_context_dataと関数名が重複していたためひとつに統一。
    # def get_context_data(self,**kwargs):
    #     context = super().get_context_data(**kwargs)
    #     store = self.get_object()
    #     context['reviews'] = Review.objects.filter(store_name=store).order_by('-create_at')
    #     return context

#予約確認画面  
class ConfirmReservation(View): #Viewクラスを継承するときは"def post"や"def get"などの関数を使用する。
    model = Reservation
    template_name = 'confirm_reservation.html'

    def get(self, request):
        context = {}
        date = ''
        time = ''
        persons =''
        restaurant_name = ''

        if 'form_date' in self.request.session:
            date = self.request.session.get('form_date')
            # 日付形式を変換
            date = datetime.strptime(date, '%Y-%m-%d').strftime('%Y年%m月%d日')
        if 'form_time' in self.request.session:
            time = self.request.session.get('form_time')
        if 'form_persons' in self.request.session:
            persons = self.request.session.get('form_persons')
        if 'form_restaurant' in self.request.session:
            restaurant_id = self.request.session.get('form_restaurant')
            restaurant = StoreInfo.objects.get(id=restaurant_id) #1店舗の情報をまるまるとっている。
            restaurant_name = restaurant.store_name

        context.update({
            'user': self.request.user,
            'date': date,
            'time': time,
            'persons': persons,
            'restaurant_name':restaurant_name,
        })

        return render(request,self.template_name,context)
    
    def post(self, request): #フォーム内のボタンが押された時に呼び出される。
        context = {}
        date = ''
        time = ''
        persons =''
        restaurant_name = ''

        if 'form_date' in self.request.session:
            date = self.request.session.get('form_date')
        if 'form_time' in self.request.session:
            time = self.request.session.get('form_time')
        if 'form_persons' in self.request.session:
            persons = self.request.session.get('form_persons')
        if 'form_restaurant' in self.request.session:
            restaurant_id = self.request.session.get('form_restaurant')
            restaurant = StoreInfo.objects.get(id=restaurant_id)
            restaurant_name = restaurant.store_name

        user_instance = self.request.user #外部キーのため
        restaurant_instance = StoreInfo.objects.get(id=restaurant_id) #外部キーのため
        # Reservation.objects.create(
        #     user=user_instance,
        #     store_name = restaurant_instance,
        #     date = date,
        #     time = time,
        #     persons = persons
        # )
        # return redirect('gourmet:reservation_success',reservation_id=Reservation.objects.create.id)

        new_reservation = Reservation.objects.create(
            user=user_instance,
            store_name=restaurant_instance,
            date=date,
            time=time,
            persons=persons
        )
        print("確認",new_reservation)

        # 新しく作成された予約のIDを使用してリダイレクト
        return redirect('gourmet:reservation_success', reservation_id=new_reservation.id)

#予約成功時に予約情報を表示するビュー 
def reservation_success(request,reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    user = reservation.user
    context = {
        'reservation':reservation,
        'user':user
    }
    return render(request, 'reservation_success.html',context)

#予約一覧表示のview
class ReserveListView(LoginRequiredMixin,generic.ListView):
    model = Reservation
    template_name = 'reserve_list.html'
    context_object_name = 'reservations' #テンプレート内で使う変数名を指定

    #ログインユーザーの予約一覧のみ表示
    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user).order_by('date') #予約日が近い順に並び替え
    
#予約キャンセル
class ReserveDeleteView(LoginRequiredMixin,DeleteView):
    model = Reservation
    success_url = reverse_lazy('gourmet:reserve_list')
    template_name = 'reservation_delete.html'
    
    #【質問】メッセージが表示されない。
    # def delete(self,request,*args,**kwargs):
    #     messages.success(self.request,"予約をキャンセルしました。")
    #     print("check",messages)
    #     return super().delete(request,*args,**kwargs)
    
    def form_valid(self,form):
        messages.success(self.request,"予約をキャンセルしました。")
        return super().form_valid(form)

    
#ユーザ情報ページ
class ProFileView(LoginRequiredMixin,UpdateView):  
    model = CustomUser
    template_name = 'profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('gourmet:profile')

    def get_object(self):
        # 現在ログインしているユーザーのオブジェクトを取得
        return self.request.user
    
#ユーザー情報編集ページ
class ProfileUpdateView(LoginRequiredMixin,UpdateView):
    model = CustomUser
    template_name = 'profile_update.html'
    form_class = ProfileForm
    success_url = reverse_lazy('gourmet:profile')

    def form_valid(self,form):
        messages.success(self.request,"ユーザー情報を更新しました。")
        return super().form_valid(form)
    
    def form_invalid(self,form):
        messages.error(self.request,"ユーザー情報の更新に失敗しました。")
        return super().form_invalid(form)
    
#レビュー投稿機能
def submit_review(request,store_id):
    store = get_object_or_404(StoreInfo, pk=store_id) #get_object_or_404(モデル, *フィルター条件)
    reviews = Review.objects.filter(store_name=store)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False) #フォームを一時保存
            review.store_name = store #外部キーであるstore_nameの値を取得
            review.save() #フォームを保存してモデルをDBに反映
            messages.success(request,'レビューのご協力ありがとうございました。')
            return redirect('gourmet:detail',pk=store.id ) #???????
    else:
        form = ReviewForm() #フォームの初期化
    
    print("reviwsの中身",reviews)
    return render(request, 'review_form.html',{'form':form,'store': store})
    
#お気に入り機能
def like_rest(request,store_id):
    store = get_object_or_404(StoreInfo, pk=store_id)

    #トグル機能(createがTrueであればLikeオブジェクトが作成される。likeにLikeオブジェクト、createdにTrue or Falseが入る。True:オブジェクトが新たに作成された/False:すでに存在しているアンパッキングの書き方。)
    like, created = Like.objects.get_or_create(user=request.user, fav=store)

    if not created:
        #すでにnot created=not True= False=すでにオブジェクトが作成済みの場合
        like.delete()
    
    print("チェック",store_id)
    
    return redirect('gourmet:detail', pk=store_id)

    
