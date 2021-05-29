from django.conf.urls import url
from booktest import views

# 在应用的url文件中进行url配置的时候
# 1 严格匹配开头和结尾
urlpatterns = [
    url(r'^$', views.index),
    url(r'^delete(\d+)/$', views.delete),  # 删除点击的图书
    url(r'^create/$', views.create),  # 新增图书
    url(r'^detail/(\d+)$', views.detail),  # 查看图书关联的英雄
    url(r'^login$', views.login),  # 显示登录页面
    url(r'^login_check$', views.login_check),  # 登录校验
    url(r'^change_pwd$', views.change_pwd),  # 修改密码页面显示
    url(r'^change_pwd_action$', views.change_pwd_action),  # 修改密码处理
    url(r'^verify_code/$', views.verify_code),  # 产生验证码图片
    url(r'^test_ajax$', views.ajax_test),  # 显示ajax页面
    url(r'^ajax_handle$', views.ajax_handle),  # ajax处理
    url(r'^login_ajax$', views.login_ajax),  # 显示ajax登录页面
    url(r'^login_ajax_check$', views.login_ajax_check),  # ajax登录请求校验
    url(r'^show_upload$', views.show_upload),  # 显示上传照片页面
    url(r'^pic_handle$', views.pic_handle),  # 上传照片处理
]
