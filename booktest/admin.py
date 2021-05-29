from django.contrib import admin
from booktest.models import BookInfo, HeroInfo, AreaInfo


# 后台管理相关文件
# Register your models here.
# 注册模型类

class BookInfoAdmin(admin.ModelAdmin):
    """图书模型管理类"""
    list_display = ['id', 'btitle', 'bpub_date']


class HeroInfoAdmin(admin.ModelAdmin):
    """英雄模型管理类"""
    list_display = ['id', 'hname', 'hgender', 'hcomment']


class AreaStackedInline(admin.StackedInline):
    """以块的形式嵌入，展示出地区的下级地区"""
    # 写多类的名字
    model = AreaInfo
    # 可以追加多少个,默认三个
    extra = 2


class AreaInfoAdmin(admin.ModelAdmin):
    """地区模型管理类"""
    list_display = ['id', 'atitle', 'title', 'parent']  # 管理页面展示出来的类容
    list_per_page = 15  # 指定每页显示15条数据
    actions_on_bottom = True
    actions_on_top = False
    list_filter = ['atitle']  # 列表右侧的过虑栏
    search_fields = ['atitle']  # 列表页上方的搜索框

    #     编辑页设置
    #     fields = ['aParent', 'atitle']  # 编辑页面字段显示顺序
    # 分组显示 fields 和 fieldsets 只能使用一个
    fieldsets = (
        ('基本', {'fields': ['atitle']}),
        ('父级', {'fields': ['aParent']})
    )

    inlines = [AreaStackedInline]


# 注册模型类
admin.site.register(BookInfo, BookInfoAdmin)
admin.site.register(HeroInfo, HeroInfoAdmin)
admin.site.register(AreaInfo, AreaInfoAdmin)
