from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django_redis import get_redis_connection
from django.conf import settings
from django.core.paginator import Paginator
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
import re

from apps.user.models import User, Address
from apps.goods.models import GoodsSKU
from apps.celery_tasks.tasks import send_register_active_email
from utils.mixin import LoginRequiredMixin
from apps.order.models import OrderInfo, OrderGoods


def register(request):
    if request.method == "GET":
        return render(request, 'register.html')

    # 接收数据
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    password2 = request.POST.get('cpwd')
    email = request.POST.get('email')
    allow = request.POST.get('allow')

    # 数据校验
    if not all([username, password, password2, email]):
        return render(request, 'register.html', {'errmsg': '数据不完整'})
    if not re.match(r'^[a-zA-Z0-9_\-]+@[a-zA-Z0-9_\-]+(\.[a-zA-Z0-9_\-]+){1,2}$', email):
        return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})
    if allow != 'on':
        return render(request, 'register.html', {'errmsg': '请统一协议'})
    # 检验用户是否存在
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    if user:
        return render(request, 'register.html', {'errmsg': '用户名已存在'})

    # 业务处理：进行用户注册，使用认证系统内置方法添加新元素
    user = User.objects.create_user(username, email, password)
    user.is_active = 0
    user.save()

    # 返回应答
    return redirect(reverse('goods:index'))


class RegisterView(View):

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        # 接收数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        password2 = request.POST.get('cpwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 数据校验
        if not all([username, password, password2, email]):
            return render(request, 'register.html', {'errmsg': '数据不完整'})
        if not re.match(r'^[a-zA-Z0-9_\-]+@[a-zA-Z0-9_\-]+(\.[a-zA-Z0-9_\-]+){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})
        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请统一协议'})
        # 检验用户是否存在
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user:
            return render(request, 'register.html', {'errmsg': '用户名已存在'})

        # 业务处理：进行用户注册，使用认证系统内置方法添加新元素
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()

        # 发送激活邮件，激活链接：http://127.0.0.1:8000/user/active/3
        # 加密用户的身份信息，生成激活token
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializer.dumps(info)
        token = token.decode('utf-8')

        # 发邮件
        send_register_active_email.delay(email, username, token)

        # 返回应答
        return redirect(reverse('goods:index'))


class ActiveView(View):
    def get(self, request, token):
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            user_id = info['confirm']

            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            return redirect(reverse('user:login'))
        except SignatureExpired:
            return HttpResponse("激活链接已过期")


class LoginView(View):
    def get(self, request):
        # 判断是否记住了用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''
        return render(request, 'login.html', {'username': username, 'checked': checked})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        if not all([username, password]):
            return render(request, 'login.html', {'errmsg': "数据不完整"})

        # 登录校验
        user = authenticate(username=username, password=password)
        if user is None:
            return render(request, 'login.html', {'errmsg': '用户名或密码错误'})
        if user.is_active:
            login(request, user)  # 记录用户的登录状态

            # 获取登陆后所有跳转的地址，默认跳转到首页
            next_url = request.GET.get('next', reverse('goods:index'))

            # 记住用户名
            response = redirect(next_url)
            remember = request.POST.get('remember')
            if remember == 'on':
                response.set_cookie('username', username)
            else:
                response.delete_cookie('username')
            return response
        return render(request, 'login.html', {'errmsg': '账户未激活'})


class LogoutView(View):
    def get(self, request):
        logout(request)  # 清除用户的session信息
        return redirect(reverse('goods:index'))


class UserInfoView(LoginRequiredMixin, View):
    """用户中心信息页"""
    def get(self, request):
        # 获取用户信息
        user = request.user
        address = Address.objects.get_default_address(user)
        # 获取历史浏览记录
        # from redis import StrictRedis
        # sr = StrictRedis(host='127.0.0.1', port='6379', password="2017916yuan", db=9)
        con = get_redis_connection('default')
        history_key = 'history_%d' % user.id

        # 获取用户最新浏览的5个商品的id
        sku_ids = con.lrange(history_key, 0, 4)

        # 从数据库中查询用户浏览的商品的具体信息
        goods_li = []
        for id in sku_ids:
            goods = GoodsSKU.objects.get(id=id)
            goods_li.append(goods)

        context = {'page': 'user',
                   'address': address,
                   'goods_li': goods_li}
        # django会自动把request.user传递给模板
        return render(request, 'user_center_info.html', context)


class UserOrderView(LoginRequiredMixin, View):
    """用户中心订单页"""
    def get(self, request, page):
        # 获取用户的订单信息
        user = request.user
        orders = OrderInfo.objects.filter(user=user).order_by('-create_time')

        # 遍历获取订单商品信息
        for order in orders:
            # 根据order_id查询订单商品信息
            order_skus = OrderGoods.objects.filter(order_id=order.order_id)
            # 遍历计算商品的小计
            for order_sku in order_skus:
                amount = order_sku.count * order_sku.price
                order_sku.amount = amount
            order.order_skus = order_skus
            order.order_status_name = OrderInfo.ORDER_STATUS[order.order_status]

        # 分页
        paginator = Paginator(orders, 1)

        try:
            page = int(page)
        except:
            page = 1
        if page > paginator.num_pages:
            page = 1

        # 获取第page页的Page实例对象
        order_page = paginator.page(page)

        # todo:进行页码的控制，页面上最多显示5个页码
        # 1.总页码小于5页，显示所有页码
        # 2.如果当前页码是前3页，显示1-5页
        # 3.如果当前页码是后3页，显示后5页
        # 4.其它情况，显示当前页的前2页，当前页，当前页的后2页
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1, num_pages + 1)
        elif page <= 3:
            pages = range(1, 6)
        elif num_pages - page < 3:
            pages = range(num_pages - 4, num_pages + 1)
        else:
            pages = range(page - 2, page + 3)

        context = {
            'order_page': order_page,
            'pages': pages,
            'page': 'order'
        }

        return render(request, 'user_center_order.html', context)


class UserSiteView(LoginRequiredMixin, View):
    """用户中心地址页"""
    def get(self, request):
        # 获取用户的默认收货地址
        user = request.user
        address = Address.objects.get_default_address(user)
        return render(request, 'user_center_site.html', {'page': 'site', 'address': address})

    def post(self, request):
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')

        if not all([receiver, addr, phone]):
            return render(request, 'user_center_site.html', {'errmsg': '信息不完整'})
        if not re.match(r'^1[34578]\d{9}$', phone):
            return render(request, 'user_center_site.html', {'errmsg': '手机号码错误'})

        user = request.user
        address = Address.objects.get_default_address(user)
        if address:
            is_default = False
        else:
            is_default = True

        # 添加新地址
        Address.objects.create(user=user,
                               receiver=receiver,
                               addr=addr,
                               zip_code=zip_code,
                               phone=phone,
                               is_default=is_default)

        return redirect(reverse('user:site'))
