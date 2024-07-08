from django.shortcuts import render,redirect,get_object_or_404
from django.views import generic
from django.views.generic import UpdateView, ListView,DeleteView,DetailView
from .models import StoreInfo,Reservation
from accounts.models import CustomUser
from .forms import ProfileForm,ReservationForm,ReviewForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


#トップページ
class TopView(generic.ListView):
    model = StoreInfo
    template_name = 'top.html'

#店舗詳細ページ
class StoreDetailView(generic.DetailView):
    model = StoreInfo
    template_name = 'store_detail.html'

    #予約フォームのデータ呼び出し(python側からTemplateに変数を渡したい場合)
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReservationForm() #get_context_dataにReservationFormを呼び出す。この'form'という変数をテンプレートで使えるようになる。
        return context
    
    #フォームから送信されたデータの処理
    def post(self, request, *args, **kwargs):
        self.object = self.get_object() #現在のStoreInfoオブジェクトを取得
        form = ReservationForm(request.POST)

        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.store_name = self.object
            reservation.save()
            return redirect('gourmet:reservation_success', reservation_id=reservation.id)
        
        #バリデーションに失敗した場合はフォームとともにテンプレートを再レンダリングする。
        return self.render_to_response(self.get_context_data(form=form))


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
class ReserveDeleteView(DeleteView):
    model = Reservation
    success_url = reverse_lazy('gourmet:reserve_list')
    template_name = 'reservation_delete.html'
    
    #【質問】メッセージが表示されない。
    def delete(self,request,*args,**kwargs):
        messages.success(self.request,"予約をキャンセルしました。")
        return super().delete(request,*args,**kwargs)
    
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
    store = get_object_or_404(StoreInfo, pk=store_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False) #フォームを一時保存
            review.store_name = store #外部キーであるstore_nameの値を取得
            review.save() #フォームを保存してモデルをDBに反映
            return redirect('gourmet:detail',pk=store.id ) #???????
    else:
        form = ReviewForm() #フォームの初期化
    return render(request, 'review_form.html',{'form':form,'store': store})
    

    
