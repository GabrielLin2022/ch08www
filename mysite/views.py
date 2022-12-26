from django.shortcuts import render, redirect
from django.http import HttpResponse
from mysite import models
from .models import Post, Mood
from .forms import ContactForm, PostForm
# Create your views here.

#pid=None, del_pass=None  針對兩變數實施"預設值設定"避免報錯 => 若無傳入則為 None
def index(request, pid=None, del_pass=None):
    # TODO 這裡是Listing 一樣功能
    #篩選 Post裡 啟用(enabled=True)，然後以建立時間(-pub_time)進行降冪排列(order_by)，[:30]表示顯示 前30筆資料(0-29)
    #指定 moods 為物件 => <QuerySet [<Mood: 開心>, <Mood: 難過>]
    #-pub_time:只要是舊的資料往下沉，新的資料會在最上面
    # 我把POST 裡面的物件 用 是否已啟用做篩選，用 出版時間，做排序，並列出前30項
    posts = models.Post.objects.filter(enabled = True).order_by('-pub_time')[:30]
    moods = models.Mood.objects.all()

    # TODO 此欄位為 CREATE - 建立貼文後，資料裡 enable = False => 要管理員手動開啟後 改成True => 所以提示才會說需要管理
    #這裡跟 posting 一樣功能
    #如果暱稱 user_id有值(不等於none)，則建立一個新的資料
    #從 form (method= 'GET')表單中拿取提交後資料(名稱連接 form裡的 input的 name)
    try:
        user_id = request.GET['user_id']
        user_pass = request.GET['user_pass']
        user_post = request.GET['user_post']
        user_mood = request.GET['mood']
    except:
        user_id = None
        message = '如要張貼訊息，則每一個欄位都要填...'

#=======================================================建立貼文
    if user_id and user_post:
        mood = Mood.objects.get(status=user_mood)
        post = Post.objects.create(
            mood = mood,
            nickname = user_id,
            del_pass = user_pass,
            message = user_post,)
        post.save()
        message = '成我儲存!請記得你的密碼[{}]!，訊息需要經過審查之後才會顯示。'.format(user_pass)

#=======================================================刪除貼文

    else:
        #真刪除
        # if pid and del_pass:
        #     post = Post.objects.get(id=pid)
        #     if post.del_pass == del_pass:
        #         post.delete()
        #         message = '資料刪除成功'
        #     else:
        #         message = '密碼錯誤'

        #偽刪除        
        if pid and del_pass:
            post = Post.objects.get(id=pid)
            if post.del_pass == del_pass:
                post.enabled = False

                post.save()
                message = '資料刪除成功'
                return redirect("index")
            else:
                message = '密碼錯誤'

#===========================================================
    # # TODO 此欄位為 DELETE - 刪除貼文(JavaScript做 刪除鈕按鍵導向，導到index這裡做刪除驗證)
    # #此地方的值來自於 base.html JavaScript的var usr = '/' + id + '/' + user_pass; 傳值到urls
    # #因為是共同一個 views.index 所以一且 del_pass, pid 有值，就會傳入 urls 執行刪除段，沒有值就會傳入預設值 None
    # #然後直接不執行 if del_pass and pid (None 屬於 False)，直接跳到 posting功能
    # if del_pass and pid:#如果不為true不執行以下程式
    #     try:
    #         #確認密碼及ID後則先到對應的 pid物件
    #         post = models.Post.objects.get(id=pid)
    #         #如果沒有找到應 pid物件則指定 post為空
    #     except:
    #         post = None
    #         #如果post確認有值(非 None)則為True
    #     if post:
    #         #張貼/刪除碼 在這裡驗證(validation)
    #         #確認填寫的刪除碼跟資料庫一樣就通過
    #         if post.del_pass == del_pass:
    #             post.delete()
    #             message = "資料刪除成功"
    #         else:
    #             message = "刪除密碼錯誤"
    # elif user_id != None:# user_id = true，create創建貼文
    #     mood = models.Mood.objects.get(status = user_mood)
    #     post = models.Post.objects.create(mood=mood, nickname=user_id, del_pass=user_pass, message=user_post)
    #     post.save()#儲存貼文
    #     message='成功儲存!請記得你的編輯密碼[{}]!，訊息需經審查後才會顯示。'.format(user_pass) 

    return render(request, 'index.html', locals())#顯示貼文
