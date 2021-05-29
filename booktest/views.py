from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from booktest.models import *
from datetime import date
from django.conf import settings
from django.core.paginator import Paginator


def login_required(view_func):
    '''登录判断装饰器'''

    def wrapper(request, *view_args, **view_kwargs):
        # 判断用户是否登录
        if request.session.has_key('islogin'):
            # 用户已登录,调用对应的视图
            return view_func(request, *view_args, **view_kwargs)
        else:
            # 用户未登录,跳转到登录页
            return redirect('/login')

    return wrapper


# 查询所有图书并显示
# request 就是HttpRequest类型的对象
# request 包含浏览器请求信息
@login_required
def index(request, pIndex):
    """显示图书信息"""
    # 1 查询所有数据
    list = BookInfo.objects.all()
    # 2 对数据进行分页
    p = Paginator(list, 10)
    # 如果当前没有传递页码信息，则认为是第一页，这样写是为了请求第一页时可以不写页码
    if pIndex == '':
        pIndex = '1'
    # 通过url匹配的参数都是字符串类型，转换成int类型
    pIndex = int(pIndex)
    # 获取第pIndex页的数据
    list2 = p.page(pIndex)
    # 获取所有的页码信息
    plist = p.page_range
    # 将当前页码、当前页的数据、页码信息传递到模板中
    # 使用模板
    return render(request, 'booktest/index.html', {'list': list2, 'plist': plist, 'pIndex': pIndex})


# 创建新图书
@login_required
def create(request):
    """创建新图书"""
    book = BookInfo()
    book.btitle = '流星蝴蝶剑'
    book.bpub_date = date(1995, 12, 30)
    book.save()
    # 转向到首页
    return redirect('/')


# 逻辑删除指定编号的图书
@login_required
def delete(request, id):
    book = BookInfo.objects.get(id=int(id))
    book.delete()
    # 转向到首页
    return redirect('/')


@login_required
def detail(request, bid):
    """查询图书关联的英雄信息"""
    # 1 通过bid查询图书信息
    book = BookInfo.objects.get(id=bid)
    # 2 查询图书关联的英雄信息
    heros = book.heroinfo_set.all()
    # 3 使用模板
    return render(request, 'booktest/detail.html', {'book': book, "heros": heros})


def login(request):
    '''显示登录页面'''
    # 判断用户是否登录
    if request.session.has_key('islogin'):
        # 用户已登录, 跳转到修改密码页面
        return redirect('/change_pwd')
    else:
        # 用户未登录
        # 获取cookie username
        if 'username' in request.COOKIES:
            # 获取记住的用户名
            username = request.COOKIES['username']
        else:
            username = ''

        return render(request, 'booktest/login.html', {'username': username})


def login_check(request):
    '''登录校验视图'''
    # 1.获取提交的用户名和密码
    username = request.POST.get('username')
    password = request.POST.get('password')
    remember = request.POST.get('remember')  # None on

    # 获取用户输入验证码
    vcode1 = request.POST.get('vcode')
    # 获取session中保存的验证码
    vcode2 = request.session.get('verifycode')

    # 进行验证码校验
    if vcode1 != vcode2:
        # 验证码错误
        return redirect('/login')

    # 2.进行登录的校验
    # 实际开发:根据用户名和密码查找数据库
    # 模拟: admin admin
    if username == 'admin' and password == 'admin':
        # 用户名密码正确，跳转到修改密码页面
        response = redirect('/change_pwd')

        # 判断是否需要记住用户名
        if remember == 'on':
            # 设置cookie username，过期时间1周
            response.set_cookie('username', username, max_age=7 * 24 * 3600)

        # 记住用户登录状态
        # 只有session中有islogin,就认为用户已登录
        request.session['islogin'] = True
        # 记住登录的用户名
        request.session['username'] = username
        # 返回应答
        return response
    else:
        # 用户名或密码错误，跳转到登录页面
        return redirect('/login')


# /change_pwd
@login_required
def change_pwd(request):
    '''显示修改密码页面'''
    # # 进行用户是否登录的判断
    # if not request.session.has_key('islogin'):
    #     # 用户未登录，跳转到登录
    #     return redirect('/login')

    return render(request, 'booktest/change_pwd.html')


# /change_pwd_action
@login_required
def change_pwd_action(request):
    '''模拟修改密码处理'''
    # # 进行用户是否登录的判断
    # if not request.session.has_key('islogin'):
    #     # 用户未登录，跳转到登录
    #     return redirect('/login')

    # 1.获取新密码
    pwd = request.POST.get('pwd')
    # 获取用户名
    username = request.session.get('username')
    # 2.实际开发的时候: 修改对应数据库中的内容...
    # 3.返回一个应答
    return redirect('/')
    # return HttpResponse('%s修改密码为:%s' % (username, pwd))


from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


def verify_code(request):
    # 引入随机函数模块
    import random
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    # font = ImageFont.truetype('FreeMono.ttf', 23)
    font = ImageFont.truetype('arial.ttf', 23)
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    # 内存文件操作
    buf = BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')


def ajax_test(request):
    """显示ajax页面"""
    return render(request, 'booktest/test_ajax.html')


def ajax_handle(request):
    """ajax请求处理"""
    # 获取传递的参数
    a = request.GET.get('a')
    # 返回的json数据 {'res': a}
    return JsonResponse({'res': a})


def login_ajax(request):
    """显示ajax登录页面"""
    return render(request, 'booktest/login_ajax.html')


def login_ajax_check(request):
    username = request.POST.get('username')
    psd = request.POST.get('password')

    # 2 进行登录的校验
    # 实际开发：根据用户名和密码查找数据库
    if username == 'admin' and psd == 'admin':
        return JsonResponse({'res': 1})
    else:
        return JsonResponse({'res': 0})


def show_upload(request):
    """显示上传图片"""
    return render(request, 'booktest/upload_pic.html')


def pic_handle(request):
    """上传图片处理"""
    # 1 获取上传的图片
    f1 = request.FILES.get('pic')
    # 2 创建一个文件
    fname = '%s/booktest/%s' % (settings.MEDIA_ROOT, f1.name)
    with open(fname, 'wb') as pic:
        # 3 获取上传文件内容并写到创建的文件中
        for c in f1.chunks():
            pic.write(c)
    # 4 在数据库中保存上传记录
    PicTest().objects.create(goods_pic='booktest/%s' % f1.name)
    # 5 返回
    return HttpResponse('OK')


def areas(request):
    """省市县选中案例"""
    return render(request, 'booktest/areas.html')


def prov(request):
    """获取所有省级数据"""
    # 1 获取所有省级地区的信息
    areas = AreaInfo.objects.filter(aParent__isnull=True)
    # 2 拼接出json数据：atitle和id
    areas_list = []
    for area in areas:
        areas_list.append((area.id, area.atitle))
    # 3 返回数据
    return JsonResponse({'data': areas_list})


def city(request, pid):
    """获取省级下级地区的数据"""
    citys = AreaInfo.objects.filter(aParent=pid)
    # 2 拼接出json数据：atitle和id
    citys_list = []
    for city in citys:
        citys_list.append((city.id, city.atitle))
    # 3 返回数据
    return JsonResponse({'data': citys_list})