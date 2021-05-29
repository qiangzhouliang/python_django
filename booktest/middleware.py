from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class BlockedIPSMiddleware(MiddlewareMixin):
    """中间件类"""
    # 中间件
    EXCLUDE_IPS = ['192.168.0.103']

    # 视图函数调运之前会调用,process_view:方法名必须写为这个
    def process_view(self, request, view_func, *view_args, **view_kwargs):
        """视图函数调运之前会调用"""
        user_ip = request.META['REMOTE_ADDR']
        if user_ip in BlockedIPSMiddleware.EXCLUDE_IPS:
            return HttpResponse('<h1>Forbidden</h1>')
