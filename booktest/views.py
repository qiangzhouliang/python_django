from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from booktest.models import *
from datetime import date


# 查询所有图书并显示
# request 就是HttpRequest类型的对象
# request 包含浏览器请求信息
def index(request):
    """显示图书信息"""
    list = BookInfo.objects.all()
    return render(request, 'booktest/index.html', {'list': list})


# 创建新图书
def create(request):
    """创建新图书"""
    book = BookInfo()
    book.btitle = '流星蝴蝶剑'
    book.bpub_date = date(1995, 12, 30)
    book.save()
    # 转向到首页
    return redirect('/')


# 逻辑删除指定编号的图书
def delete(request, id):
    book = BookInfo.objects.get(id=int(id))
    book.delete()
    # 转向到首页
    return redirect('/')


def detail(request, bid):
    """查询图书关联的英雄信息"""
    # 1 通过bid查询图书信息
    book = BookInfo.objects.get(id=bid)
    # 2 查询图书关联的英雄信息
    heros = book.heroinfo_set.all()
    # 3 使用模板
    return render(request, 'booktest/detail.html', {'book': book, "heros": heros})


def login(request):
    """显示登录页面"""
    return render(request, 'booktest/login.html')


def login_check(request):
    """登录校验试图"""
    # request.POST 保存的是post请求参数
    # request.GET 保存的是get请求的参数
    # 1 获取提交的用户名和密码
    username = request.POST.get('username')
    psd = request.POST.get('password')
    # 2 进行登录的校验
    # 实际开发：根据用户名和密码查找数据库
    if username == 'admin' and psd == 'admin':
        return redirect('/')
    else:
        return redirect('/login')


def ajax_test(request):
    """显示ajax页面"""
    return render(request, 'booktest/test_ajax.html')


def ajax_handle(request):
    """ajax请求处理"""
    # 获取传递的参数
    a = request.GET.get('a')
    # 返回的json数据 {'res': a}
    return JsonResponse({'res': a})