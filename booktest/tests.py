from django.test import TestCase
from booktest.models import BookInfo
from booktest.models import HeroInfo
from datetime import date

# Create your tests here.
b = BookInfo()

b.btitle = "天龙八部"
b.bpub_date = date(1990, 1, 1)
#保存数据
b.save()

# 查询数据
b2 = BookInfo.objects.get(id=1)

# 修改
b2.bpub_date = date(1990, 10, 10)

# 删除
b2.delete()

# 关联关系
h=HeroInfo()
h.hname='a1'
h.hgender=False
h.hbook=b
h.save()

# 查询
b.heroinfo_set.all()
