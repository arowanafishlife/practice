from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Message,Good,Following,Profile_text
from .forms import MyPostForm

# timelineのビュー関数
@login_required(login_url='/admin/login/')
def timeline(request, page=1):
    # POST送信の処理
    if request.method == 'POST':
        # 送信内容の取得
        content = request.POST['content']
        # Messageを作成し設定して保存
        msg = Message()
        msg.owner = request.user
        msg.content = content
        msg.save()
        # メッセージを設定
        messages.success(request, '新しいメッセージを投稿しました！')
        return redirect(to='/sns/timeline')
    # GETアクセス時の処理
    else:
        form = MyPostForm()

    # Followingのリストを取得
    fls = Following.objects.filter(owner=request.user)
    # フォロー先のtargetのリストを取得
    targetlist = [request.user]
    for item in fls:
        targetlist.append(item.target)
    # targetのメッセージの取得
    tl_messages = get_your_timeline_message(targetlist, page)

    # 共通処理
    params = {
        'login_user':request.user,
        'contents':tl_messages,
        'form':form,
    }
    return render(request, 'sns/timeline.html', params)


# 指定されたtargetlistによるMessageの取得
def get_your_timeline_message(targetlist, page):
    page_num = 10 #ページあたりの表示数
    # ownerがtargetlistに含まれるMessageの取得
    messages = Message.objects.filter(owner__in=targetlist)
    # ページネーションで指定ページを取得
    page_item = Paginator(messages, page_num)
    return page_item.get_page(page)


# goodボタンの処理
@login_required(login_url='/admin/login/')
def good(request, good_id):
    # goodするMessageを取得
    good_msg = Message.objects.get(id=good_id)
    # 自分がメッセージにGoodした数を調べる
    is_good = Good.objects.filter(owner=request.user) \
            .filter(message=good_msg).count()
    # ゼロより大きければ既にgood済み
    if is_good > 0:
        messages.success(request, '既にメッセージにはGoodしています。')
        return redirect(to='/sns/timeline')
    
    # Messageのgood_countを１増やす
    good_msg.good_count += 1
    good_msg.save()
    # Goodを作成し、設定して保存
    good = Good()
    good.owner = request.user
    good.message = good_msg
    good.save()
    # メッセージを設定
    messages.success(request, 'メッセージにGoodしました！')
    return redirect(to='/sns/timeline')


# share時のtimelineのビュー関数
@login_required(login_url='/admin/login/')
def share_timeline(request, share_id, page=1):
    # シェアするMessageの取得
    share = Message.objects.get(id=share_id)
    # POST送信の処理
    if request.method == 'POST':
        # 送信内容の取得
        content = request.POST['content']
        # Messageを作成し設定して保存
        msg = Message()
        msg.owner = request.user
        msg.content = content
        msg.share_id = share.id
        msg.save()
        share_msg = msg.get_share()
        share_msg.share_count += 1
        share_msg.save()
        # メッセージを設定
        messages.success(request, '新しいメッセージを投稿しました！')
        return redirect(to='/sns/timeline')
    # GETアクセス時の処理
    else:
        form = MyPostForm()

    # Followingのリストを取得
    fls = Following.objects.filter(owner=request.user)
    # フォロー先のtargetのリストを取得
    targetlist = [request.user]
    for item in fls:
        targetlist.append(item.target)
    # targetのメッセージの取得
    tl_messages = get_your_timeline_message(targetlist, page)

    # 共通処理
    params = {
        'login_user':request.user,
        'contents':tl_messages,
        'form':form,
        'share':share,
    }
    return render(request, 'sns/share_timeline.html', params)


# globalのビュー関数
@login_required(login_url='/admin/login/')
def global_TL(request, page=1):
    # POST送信の処理
    if request.method == 'POST':
        # 送信内容の取得
        content = request.POST['content']
        # Messageを作成し設定して保存
        msg = Message()
        msg.owner = request.user
        msg.content = content
        msg.save()
        # メッセージを設定
        messages.success(request, '新しいメッセージを投稿しました！')
        return redirect(to='/sns/global_TL')
    # GETアクセス時の処理
    else:
        form = MyPostForm()
    
    page_num = 10 #ページあたりの表示数
    # 全てのMessageの取得
    allmessages = Message.objects.all()
    # ページネーションで指定ページを取得
    page_item = Paginator(allmessages, page_num)
    tl_messages = page_item.get_page(page)

    # 共通処理
    params = {
        'login_user':request.user,
        'contents':tl_messages,
        'form':form,
    }
    return render(request, 'sns/global_TL.html', params)


# share時のglobalのビュー関数
@login_required(login_url='/admin/login/')
def share_global_TL(request, share_id, page=1):
    # シェアするMessageの取得
    share = Message.objects.get(id=share_id)
    # POST送信の処理
    if request.method == 'POST':
        # 送信内容の取得
        content = request.POST['content']
        # Messageを作成し設定して保存
        msg = Message()
        msg.owner = request.user
        msg.content = content
        msg.share_id = share.id
        msg.save()
        share_msg = msg.get_share()
        share_msg.share_count += 1
        share_msg.save()
        # メッセージを設定
        messages.success(request, '新しいメッセージを投稿しました！')
        return redirect(to='/sns/global_TL')
    # GETアクセス時の処理
    else:
        form = MyPostForm()

    page_num = 10 #ページあたりの表示数
    # 全てのMessageの取得
    allmessages = Message.objects.all()
    # ページネーションで指定ページを取得
    page_item = Paginator(allmessages, page_num)
    tl_messages = page_item.get_page(page)

    # 共通処理
    params = {
        'login_user':request.user,
        'contents':tl_messages,
        'form':form,
        'share':share,
    }
    return render(request, 'sns/share_global_TL.html', params)


# profileのビュー関数
@login_required(login_url='/admin/login/')
def profile(request, target_id, page=1):

    # プロフィールを表示する対象Userの取得
    target = User.objects.get(id=target_id)

    # targetがフォロー中のUserの取得
    flings = Following.objects.filter(owner=target)
    target_followings = []
    for f in flings:
        target_followings.append(f.target)

    # targetのフォロワーのUserの取得
    fled = Following.objects.filter(target=target)
    target_followed = []
    for f in fled:
        target_followed.append(f.owner)

    # targetがこれまでに投稿したメッセージの取得
    targetlist = [target]
    tl_messages = get_your_timeline_message(targetlist, page)

    # targetのProfile_textの取得
    protext = Profile_text.objects.filter(owner=target)
    if protext.count()==0:
        create_default_profile(target)
        protext_content = Profile_text.objects.get(owner=target).content
    else:
        protext_content = protext.first().content

    if target==request.user:
        updatable = True
    else:
        updatable = False

    if target==request.user:
        isflw = -1
    elif Following.objects.filter(owner=request.user, target=target).count() > 0:
        isflw = 1
    else:
        isflw = 0

    # 共通処理
    params = {
        'login_user':request.user,
        'target_user':target,

        'followings':target_followings,
        'following_size':len(target_followings),
        'followed':target_followed,
        'followed_size':len(target_followed),

        'contents':tl_messages,

        'profile_text':protext_content,
        'pftext_updatable':updatable,

        'is_following':isflw
    }
    return render(request, 'sns/profile.html', params)


# followingのビュー関数
@login_required(login_url='/admin/login/')
def following(request, target_id):
    target = User.objects.get(id=target_id)

    flings = Following.objects.filter(owner=target)
    target_followings = []
    for f in flings:
        target_followings.append(f.target)

    pfs = []
    for f in flings:
        s = Profile_text.objects.filter(owner=f.target)
        if s.count() > 0:
            p = s.first()
        else:
            create_default_profile(f.target)
            p = Profile_text.objects.get(owner=f.target)
        pfs.append(p)

    # 共通処理
    params = {
        'login_user':request.user,
        'target_user':target,

        'followings':target_followings,
        'following_size':len(target_followings),
        'profiles':pfs,
    }
    return render(request, 'sns/following.html', params)


# followedのビュー関数
@login_required(login_url='/admin/login/')
def followed(request, target_id):
    target = User.objects.get(id=target_id)

    fled = Following.objects.filter(target=target)
    target_followed = []
    for f in fled:
        target_followed.append(f.owner)

    pfs = []
    for f in fled:
        s = Profile_text.objects.filter(owner=f.owner)
        if s.count() > 0:
            p = s.first()
        else:
            create_default_profile(f.target)
            p = Profile_text.objects.get(owner=f.owner)
        pfs.append(p)

    # 共通処理
    params = {
        'login_user':request.user,
        'target_user':target,

        'followed':target_followed,
        'followed_size':len(target_followed),
        'profiles':pfs,
    }
    return render(request, 'sns/followed.html', params)


# update_profileのビュー関数
@login_required(login_url='/admin/login/')
def update_profile(request, target_id, page=1):
     # プロフィールを表示する対象Userの取得
    target = User.objects.get(id=target_id)

    # Profile_text更新時の処理
    if request.method == 'POST':
        # 送信内容の取得
        content = request.POST['content']
        # Profile_textを作成または更新して保存
        pftxt = Profile_text.objects.get(owner=target)
        pftxt.content = content
        pftxt.save()
        # メッセージを設定
        messages.success(request, 'プロフィール文を更新しました！')
        return redirect(to='/sns/profile/'+str(target_id)+'/')
    # GETアクセス時の処理
    else:
        form = MyPostForm()

    # targetがフォロー中のUserの取得
    flings = Following.objects.filter(owner=target)
    target_followings = []
    for f in flings:
        target_followings.append(f.target)

    # targetのフォロワーのUserの取得
    fled = Following.objects.filter(target=target)
    target_followed = []
    for f in fled:
        target_followed.append(f.owner)

    # targetがこれまでに投稿したメッセージの取得
    targetlist = [target]
    tl_messages = get_your_timeline_message(targetlist, page)

    # targetのProfile_textの取得
    protext = Profile_text.objects.filter(owner=target)
    if protext.count()==0:
        protext_content = 'プロフィールが未入力です。'
    else:
        protext_content = protext.first().content


    # 共通処理
    params = {
        'login_user':request.user,
        'target_user':target,

        'followings':target_followings,
        'following_size':len(target_followings),
        'followed':target_followed,
        'followed_size':len(target_followed),

        'contents':tl_messages,

        'profile_text':protext_content,

        'form':form,
    }
    return render(request, 'sns/update_profile.html', params)


# create_followingのビュー関数
@login_required(login_url='/admin/login/')
def create_following(request, target_id):
    flw = Following()
    flw.owner = request.user
    flw.target = User.objects.get(id=target_id)
    flw.save()
    # メッセージを設定
    messages.success(request, str(flw.target)+'をフォローしました！')
    return redirect(to='/sns/profile/'+str(target_id)+'/')


# delete_followingのビュー関数
@login_required(login_url='/admin/login/')
def delete_following(request, target_id):
    target = User.objects.get(id=target_id)
    flw = Following.objects.get(owner=request.user, target=target)
    flw.delete()
    # メッセージを設定
    messages.success(request, str(flw.target)+'をフォロー解除しました！')
    return redirect(to='/sns/profile/'+str(target_id)+'/')


# UserのProfile_textが存在しない場合、初期値で生成する関数
def create_default_profile(target):
    pf = Profile_text()
    pf.owner = target
    pf.content = 'プロフィールが未入力です。'
    pf.save()