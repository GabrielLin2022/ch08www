from django.contrib import admin
from mysite import models
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display=('id','nickname', 'message', 'enabled', 'pub_time','mood','del_pass')#可以從後台看到你想看到的資料，在這裡設定
    ordering=('-pub_time',)#倒著數，這樣才不會54321

admin.site.register(models.Mood)
admin.site.register(models.Post, PostAdmin)

