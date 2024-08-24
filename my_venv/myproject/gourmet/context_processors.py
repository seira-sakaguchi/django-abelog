# コンテキストプロセッサのメリット
# 再利用性: データを一度設定すれば、すべてのテンプレートで再利用できる。
# コードの簡潔さ: 各ビューで同じデータを設定する必要がなく、コードがすっきり！

def member_status(request):
    #ユーザーがログインしている場合
    if request.user.is_authenticated:
        from gourmet.models import Member
        #memberモデルのユーザー名と現在のユーザー名が一致し、存在していたら(有料会員にすでに登録済みならば)
        is_member = Member.objects.filter(user=request.user).exists()
        return {'is_member': is_member}
    return {'is_member': False}