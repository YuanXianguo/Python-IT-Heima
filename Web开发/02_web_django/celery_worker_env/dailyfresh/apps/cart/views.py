from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django_redis import get_redis_connection

from apps.goods.models import GoodsSKU
from utils.mixin import LoginRequiredMixin

# 添加商品到购物车
# 1)请求方式，采用ajax post
# 如果涉及到数据的修改（新增，更新，删除），采用post
# 如果只涉及到数据的获取，采用get
# 2)传递参数：商品id 商品数量


# /cart/add
class CartAddView(View):

    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 0, 'errmsg': '请先登录'})
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')

        # 数据完整性校验
        if not all([sku_id, count]):
            return JsonResponse({'res': 1, 'errmsg': '数据不完整'})
        try:
            count = int(count)
        except:
            return JsonResponse({'res': 2, 'errmsg': '商品数目错误'})
        # 校验商品是否存在
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({'res': 3, 'errmsg': '商品不存在'})

        # 业务处理：添加购物车记录
        # 先尝试获取sku_id的值
        con = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id
        # 如果不存在，返回none
        cart_count = con.hget(cart_key, sku_id)
        if cart_key:
            # 累加
            if cart_count:  # 不为空
                count += int(cart_count)

        # 校验库存
        if count > sku.stock:
            return JsonResponse({'res': 4, 'errmsg': '商品库存不足'})

        # 设置hash中sku_id对应的值
        con.hset(cart_key, sku_id, count)

        # 计算用户购物车商品的条目数
        total_count = con.hlen(cart_key)
        return JsonResponse({'res': 5, 'total_count': total_count, 'message': '添加成功'})


class CartInfoView(LoginRequiredMixin, View):
    """购物车页面显示"""
    def get(self, request):
        user = request.user
        con = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id
        cart_dict = con.hgetall(cart_key)

        skus = list()
        total_count = 0
        total_amount = 0
        for sku_id, count in cart_dict.items():
            sku = GoodsSKU.objects.get(id=sku_id)
            # 给sku动态增加小计和数量属性
            sku.count = int(count)
            amount = int(count) * sku.price
            sku.amount = amount
            skus.append(sku)

            total_count += int(count)
            total_amount += amount

        context = {
            'skus': skus,
            'total_count': total_count,
            'total_amount': total_amount
        }
        return render(request, 'cart.html', context)


class CartUpdateView(View):

    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 0, 'errmsg': '请先登录'})
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')

        # 数据完整性校验
        if not all([sku_id, count]):
            return JsonResponse({'res': 1, 'errmsg': '数据不完整'})
        try:
            count = int(count)
        except:
            return JsonResponse({'res': 2, 'errmsg': '商品数目错误'})
        # 校验商品是否存在
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({'res': 3, 'errmsg': '商品不存在'})

        # 业务处理
        con = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id

        # 校验库存
        if count > sku.stock:
            return JsonResponse({'res': 4, 'errmsg': '商品库存不足'})

        con.hset(cart_key, sku_id, count)

        # 计算用户购物车中商品的总件数
        vals = con.hvals(cart_key)
        total_count = sum(list(map(int, vals)))

        return JsonResponse({'res': 5, 'total_count': total_count, 'message': '更新成功'})


class CartDeleteView(View):
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 0, 'errmsg': '请先登录'})
        sku_id = request.POST.get('sku_id')

        # 数据完整性校验
        if not sku_id:
            return JsonResponse({'res': 1, 'errmsg': '数据不完整'})

        # 校验商品是否存在
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({'res': 2, 'errmsg': '商品不存在'})

        # 业务处理
        con = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id
        con.hdel(cart_key, sku_id)

        # 计算用户购物车中商品的总件数
        vals = con.hvals(cart_key)
        total_count = sum(list(map(int, vals)))

        return JsonResponse({'res': 3,  'total_count': total_count, 'message': '删除成功'})

