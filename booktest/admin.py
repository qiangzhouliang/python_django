from django.contrib import admin
from booktest.models import BookInfo, HeroInfo


# 后台管理相关文件
# Register your models here.
# 注册模型类

class BookInfoAdmin(admin.ModelAdmin):
    """图书模型管理类"""
    list_display = ['id', 'btitle', 'bpub_date']


class HeroInfoAdmin(admin.ModelAdmin):
    """英雄模型管理类"""
    list_display = ['id', 'hname', 'hgender', 'hcomment']


# 注册模型类
admin.site.register(BookInfo, BookInfoAdmin)
admin.site.register(HeroInfo, HeroInfoAdmin)
