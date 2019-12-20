from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from django.core.cache import cache
from django_redis import get_redis_connection
from django.core.paginator import Paginator

from apps.goods.models import GoodsType, GoodsSKU, IndexGoodsBanner, IndexPromotionBanner, IndexTypeGoodsBanner
from apps.order.models import OrderGoods


class IndexView(View):
    def get(self, request):
        # 尝试从缓存中获取数据
        context = cache.get('index_page_data')

        if context is None:
            # 获取商品的种类信息
            types = GoodsType.objects.all()

            # 获取首页轮播商品信息
            goods_banners = IndexGoodsBanner.objects.all().order_by('index')

            # 获取首页促销活动信息
            promotion_banners = IndexPromotionBanner.objects.all().order_by('index')

            for type in types:
                # 获取首页分类商品图片展示信息
                image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1)
                # 获取首页分类商品文字展示信息
                title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0)

                # 给type动态添加属性
                type.image_banners = image_banners
                type.title_banners = title_banners

            context = {
                'types': types,
                'goods_banners': goods_banners,
                'promotion_banners': promotion_banners,
            }

            # 设置缓存 key value timeout
            cache.set('index_page_data', context, 3600)

        # 获取用户购物车中商品的数目
        user = request.user
        cart_count = 0

        if user.is_authenticated:
            con = get_redis_connection('default')
            cart_key = 'cart_%d' % user.id
            cart_count = con.hlen(cart_key)

        context.update(cart_count=cart_count)

        return render(request, 'index.html', context)


class DetailView(View):
    def get(self, request, goods_id):
        try:
            sku = GoodsSKU.objects.get(id=goods_id)
        except GoodsSKU.DoesNotExist:
            return redirect(reverse('goods:index'))
        # 获取商品的分类信息
        types = GoodsType.objects.all()

        # 获取商品的评论信息
        sku_orders = OrderGoods.objects.filter(sku=sku).exclude(comment='')

        # 获取新品信息
        new_skus = GoodsSKU.objects.filter(type=sku.type).order_by('-create_time')[:2]

        # 获取同一个SPU的其它规格商品
        same_spu_skus = GoodsSKU.objects.filter(goods=sku.goods).exclude(id=goods_id)

        # 获取用户购物车中商品的数目
        user = request.user
        cart_count = 0
        if user.is_authenticated:
            con = get_redis_connection('default')
            cart_key = 'cart_%d' % user.id
            cart_count = con.hlen(cart_key)

            # 添加用户的历史记录
            history_id = 'history_%d' % user.id
            # 移出列表中的goods_id：key count(0表示移出所有) value
            con.lrem(history_id, 0, goods_id)
            # 把goods_id插入到列表的左侧
            con.lpush(history_id, goods_id)
            # 只保留5最新5条记录
            con.ltrim(history_id, 0, 4)

        context = {
            'sku': sku,
            'types': types,
            'sku_orders': sku_orders,
            'new_skus': new_skus,
            'same_spu_skus': same_spu_skus,
            'cart_count': cart_count
        }
        return render(request, 'detail.html', context)


# 种类id，页码，排序方式 /list/种类id/页码?sort=排序方式
class ListView(View):
    def get(self, request, type_id, page):
        # 获取种类信息
        try:
            type = GoodsType.objects.get(id=type_id)
        except GoodsType.DoesNotExist:
            return redirect(reverse('goods:index'))

        # 获取分类信息
        types = GoodsType.objects.all()

        # 获取分类商品的信息
        # 获取排序的方式
        # sort=default/price/sales
        sort = request.GET.get('sort')
        if sort == 'price':
            skus = GoodsSKU.objects.filter(type=type).order_by('price')
        elif sort == 'sales':
            skus = GoodsSKU.objects.filter(type=type).order_by('-sales')
        else:
            sort = 'default'
            skus = GoodsSKU.objects.filter(type=type).order_by('-id')

        # 对数据进行分页
        paginator = Paginator(skus, 1)

        try:
            page = int(page)
        except:
            page = 1
        if page > paginator.num_pages:
            page = 1

        # 获取第page页的Page实例对象
        skus_page = paginator.page(page)

        # todo:进行页码的控制，页面上最多显示5个页码
        # 1.总页码小于5页，显示所有页码
        # 2.如果当前页码是前3页，显示1-5页
        # 3.如果当前页码是后3页，显示后5页
        # 4.其它情况，显示当前页的前2页，当前页，当前页的后2页
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1, num_pages+1)
        elif page <= 3:
            pages = range(1, 6)
        elif num_pages - page < 3:
            pages = range(num_pages-4, num_pages+1)
        else:
            pages = range(page-2, page+3)

        # 获取新品信息
        new_skus = GoodsSKU.objects.filter(type=type).order_by('-create_time')[:2]

        # 获取用户购物车中商品的数目
        user = request.user
        cart_count = 0

        if user.is_authenticated:
            con = get_redis_connection('default')
            cart_key = 'cart_%d' % user.id
            cart_count = con.hlen(cart_key)

        context = {
            'type': type,
            'types': types,
            'skus_page': skus_page,
            'new_skus': new_skus,
            'cart_count': cart_count,
            'pages': pages,
            'sort': sort
        }
        return render(request, 'list.html', context)
