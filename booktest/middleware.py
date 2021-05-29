from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


# process_request:是在产生request对象，进行url匹配之前调用。
# process_view：是url匹配之后，调用视图函数之前。
# process_response：视图函数调用之后，内容返回给浏览器之前。
# process_exception:视图函数出现异常，会调用这个函数。
# 如果注册的多个中间件类中包含process_exception函数的时候，调用的顺序跟注册的顺序是相反的。
class BlockedIPSMiddleware(MiddlewareMixin):
    """中间件类"""
    # 中间件
    EXCLUDE_IPS = ['192.168.0.103']

    # 初始化：无需任何参数，服务器响应第一个请求的时候调用一次，用于确定是否启用当前中间件。
    def __init__(self, get_response):
        self.get_response = get_response

    # 处理请求前：在每个请求上，request对象产生之后，url匹配之前调用，返回None或HttpResponse对象。
    def process_request(self, request):
        pass

    # 视图函数调运之前会调用,process_view:方法名必须写为这个
    # 处理视图前：在每个请求上，url匹配之后，视图函数调用之前调用，返回None或HttpResponse对象。
    def process_view(self, request, view_func, *view_args, **view_kwargs):
        """视图函数调运之前会调用"""
        user_ip = request.META['REMOTE_ADDR']
        if user_ip in BlockedIPSMiddleware.EXCLUDE_IPS:
            return HttpResponse('<h1>Forbidden</h1>')

    # 处理响应后：视图函数调用之后，所有响应返回浏览器之前被调用，在每个请求上调用，返回HttpResponse对象。
    def process_response(self, request, response):
        return response
