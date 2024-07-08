from django import forms

from  accounts.models import CustomUser #accounts.models.pyのクラスを継承する。
from .models import Reservation,Review

#ユーザー情報
class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('full_name','furigana','email','postal_code','address','phone_number') #accounts/models.pyのフィールドのデータを参照

    #全フォームフィールドに一括でBootstrapのform-controlクラスを追加できる。
    def __init__(self,*args,**kwargs):  
        super().__init__(*args,**kwargs)
        for field in self.fields.values(): #selfはインスタンス化されたクラス自身
            field.widget.attrs['class'] = 'form-control' 


#予約フォーム
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date', 'time', 'persons']
        widgets = {
            'date': forms.TextInput(attrs={'class': 'form-control fieldset__input js__datepicker', 'placeholder': '予約の日付を選択してください。'}),
            'time': forms.TextInput(attrs={'class': 'form-control fieldset__input js__timepicker', 'placeholder': '予約の時間を選択してください。'}),
            'persons': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('', '予約人数を選択してください'),
                (1, '1名'),
                (2, '2名'),
                (3, '3名'),
                (4, '4名'),
                (5, '5名以上')
            ])
        }

#レビューフォーム
class ReviewForm(forms.ModelForm):
    score = forms.ChoiceField(
        label = 'お店の評価をしてください。',
        choices = Review.SCORE_CHOICES,
        widget = forms.RadioSelect
    )

    class Meta:
        model = Review
        fields = ['score','handle','title','content']

    def __init__(self,*args,**kwargs):  
        super().__init__(*args,**kwargs)
        self.fields['handle'].widget.attrs['class']='form-control'
        self.fields['handle'].widget.attrs['placeholder']='ニックネームを入力してください。'
        self.fields['title'].widget.attrs['class']='form-control'
        self.fields['title'].widget.attrs['placeholder']='タイトルを入力してください。'
        self.fields['content'].widget.attrs['class']='form-control'
        self.fields['content'].widget.attrs['placeholder']='口コミの内容を入力してください。'

