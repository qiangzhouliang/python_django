from django.db import models


# 设计和表对应的类，模型类
# Create your models here.

from django.db import models


# 设计和表对应的类，模型类
# Create your models here.

from django.db import models


# 设计和表对应的类，模型类
# Create your models here.

# 定义图书模型类BookInfo
class BookInfo(models.Model):
    btitle = models.CharField(max_length=20)  # 图书名称
    bpub_date = models.DateField()  # 发布日期
    bread = models.IntegerField(default=0)  # 阅读量
    bcomment = models.IntegerField(default=0)  # 评论量
    isDelete = models.BooleanField(default=False)  # 逻辑删除

    class Meta:
        db_table = 'bookinfo'  # 指定模型类对应的表名


# 定义英雄模型类HeroInfo
class HeroInfo(models.Model):
    hname = models.CharField(max_length=20)  # 英雄姓名
    hgender = models.BooleanField(default=True)  # 英雄性别
    isDelete = models.BooleanField(default=False)  # 逻辑删除
    hcomment = models.CharField(max_length=200)  # 英雄描述信息
    hbook = models.ForeignKey('BookInfo', on_delete=models.CASCADE)  # 英雄与图书表的关系为一对多，所以属性定义在英雄模型类中

    class Meta:
        db_table = 'heroinfo'  # 指定模型类对应的表名


class AreaInfo(models.Model):
    """地址模型类"""
    # 地区名称,verbose_name 显示的标题
    atitle = models.CharField(verbose_name='标题', max_length=20)
    # 自关联属性
    aParent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.atitle

    def title(self):
        return self.atitle
    title.admin_order_field = 'atitle'  # 给title方法添加点击排序
    title.short_description = '地区名称'  # 指定列的标题

    def parent(self):
        """返回父地区的标题"""
        if self.aParent is None:
            return ''
        else:
            return self.aParent.atitle
    parent.short_description = '父级地区名称'