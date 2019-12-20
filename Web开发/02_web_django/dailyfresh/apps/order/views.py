from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from django_redis import get_redis_connection
from django.db import transaction
from django.http import JsonResponse
from datetime import datetime
from alipay import AliPay, ISVAliPay
import os

from apps.goods.models import GoodsSKU
from apps.user.models import Address
from utils.mixin import LoginRequiredMixin
from apps.order.models import OrderInfo, OrderGoods
from django.conf import settings


class OrderPlaceView(LoginRequiredMixin, View):
    """订单提交"""
    def post(self, request):

        # 获取用户
        user = request.user

        # 获取参数
        sku_ids = request.POST.getlist('sku_ids')

        # 校验参数
        if not sku_ids:
            return redirect(reverse('cart:cart'))

        # 获取地址
        addrs = Address.objects.filter(user=user)

        # 遍历获取提交商品信息
        con = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id

        skus = list()
        total_count = 0
        total_amount = 0
        for sku_id in sku_ids:
            sku = GoodsSKU.objects.get(id=sku_id)  # 查询对应sku
            count = con.hget(cart_key, sku_id)  # 从redis获取sku对应的数量
            count = int(count)
            amount = sku.price * count  # 计算对应小计
            total_count += count
            total_amount += amount
            # 动态添加属性
            sku.count = count
            sku.amount = amount
            skus.append(sku)

        # 运费，实际开发属于一个子系统
        transit_price = 10

        # 实付款
        total_pay = total_amount + transit_price

        context = {
            'addrs': addrs,
            'skus': skus,
            'total_count': total_count,
            'total_amount': total_amount,
            'transit_price': transit_price,
            'total_pay': total_pay,
            'sku_ids': ','.join(sku_ids)
        }

        return render(request, 'place_order.html', context)


class OrderCommitView1(View):
    """订单创建"""
    @transaction.atomic
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 0, 'errmsg': '请登陆'})

        # 获取信息
        addr_id = request.POST.get('addr_id')
        pay_method = request.POST.get('pay_method')
        sku_ids = request.POST.get('sku_ids').split(',')

        # 校验完整性
        if not all([addr_id, pay_method, sku_ids]):
            return JsonResponse({'res': 1, 'errmsg': '数据不完整'})

        # 校验支付方式
        if pay_method not in OrderInfo.PAY_METHODS.keys():
            return JsonResponse({'res': 2, 'errmsg': '非法支付方式'})

        # 校验地址
        try:
            addr = Address.objects.get(id=addr_id)
        except Address.DoesNotExist:
            return JsonResponse({'res': 3, 'errmsg': '地址非法'})

        # todo：创建订单核心业务

        # todo:向df_order_info表中添加一条记录
        order_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(user.id)
        transit_price = 10
        total_count = 0
        total_price = 0

        # 设置事务保存点
        save_id = transaction.savepoint()

        try:
            order = OrderInfo.objects.create(
                order_id=order_id,
                user=user,
                addr=addr,
                pay_method=pay_method,
                total_count=total_count,
                total_price=total_price,
                transit_price=transit_price
            )

            # todo:用户的订单中有几个商品，需要向df_order_goods表中添加几条数据
            con = get_redis_connection('default')
            cart_key = 'cart_%d' % user.id
            for sku_id in sku_ids:
                try:
                    # sku = GoodsSKU.objects.get(id=sku_id)  # 查询对应sku
                    # 添加悲观锁
                    # select * from df_goods_sku where id=17 for update;
                    sku = GoodsSKU.objects.select_for_update().get(id=sku_id)
                except:
                    transaction.savepoint_rollback(save_id)
                    return JsonResponse({'res': 4, 'errmsg': '商品不存在'})

                count = con.hget(cart_key, sku_id)  # 从redis获取sku对应的数量

                # todo:判断商品的库存
                if int(count) > sku.stock:
                    transaction.savepoint_rollback(save_id)
                    return JsonResponse({'res': 6, 'errmsg': '库存不足'})

                OrderGoods.objects.create(
                    order=order,
                    sku=sku,
                    count=count,
                    price=sku.price
                )

                # todo:更新商品的库存和销量
                sku.stock -= int(count)
                sku.sales += int(count)
                sku.save()

                # todo:累加计算订单商品的总数量和总价格
                amount = sku.price * int(count)
                total_count += int(count)
                total_price += amount

            # todo:更新订单信息表中的总数量和总价格
            order.total_count = total_count
            order.total_price = total_price
            order.save()
        except:
            transaction.savepoint_rollback(save_id)
            return JsonResponse({'res': 7, 'errmsg': '下单失败'})

        # 提交事务
        transaction.savepoint_commit(save_id)

        # todo:清除用户购物车中对应的记录
        con.hdel(cart_key, *sku_ids)

        return JsonResponse({'res': 5, 'message': '添加成功'})


class OrderCommitView(View):
    """订单创建"""
    @transaction.atomic
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 0, 'errmsg': '请登陆'})

        # 获取信息
        addr_id = request.POST.get('addr_id')
        pay_method = request.POST.get('pay_method')
        sku_ids = request.POST.get('sku_ids').split(',')

        # 校验完整性
        if not all([addr_id, pay_method, sku_ids]):
            return JsonResponse({'res': 1, 'errmsg': '数据不完整'})

        # 校验支付方式
        if pay_method not in OrderInfo.PAY_METHODS.keys():
            return JsonResponse({'res': 2, 'errmsg': '非法支付方式'})

        # 校验地址
        try:
            addr = Address.objects.get(id=addr_id)
        except Address.DoesNotExist:
            return JsonResponse({'res': 3, 'errmsg': '地址非法'})

        # todo：创建订单核心业务

        # todo:向df_order_info表中添加一条记录
        order_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(user.id)
        transit_price = 10
        total_count = 0
        total_price = 0

        # 设置事务保存点
        save_id = transaction.savepoint()

        try:
            order = OrderInfo.objects.create(
                order_id=order_id,
                user=user,
                addr=addr,
                pay_method=pay_method,
                total_count=total_count,
                total_price=total_price,
                transit_price=transit_price
            )

            # todo:用户的订单中有几个商品，需要向df_order_goods表中添加几条数据
            con = get_redis_connection('default')
            cart_key = 'cart_%d' % user.id
            for sku_id in sku_ids:
                for i in range(3):
                    try:
                        sku = GoodsSKU.objects.get(id=sku_id)  # 查询对应sku
                        # 添加悲观锁
                        # select * from df_goods_sku where id=17 for update;
                        # sku = GoodsSKU.objects.select_for_update().get(id=sku_id)
                    except:
                        transaction.savepoint_rollback(save_id)
                        return JsonResponse({'res': 4, 'errmsg': '商品不存在'})

                    count = con.hget(cart_key, sku_id)  # 从redis获取sku对应的数量

                    # todo:判断商品的库存
                    if int(count) > sku.stock:
                        transaction.savepoint_rollback(save_id)
                        return JsonResponse({'res': 6, 'errmsg': '库存不足'})

                    # todo:更新商品的库存和销量
                    # sku.stock -= int(count)
                    # sku.sales += int(count)
                    # sku.save()
                    origin_stock = sku.stock
                    new_stock = origin_stock - int(count)
                    new_sales = sku.sales + int(count)

                    # update.df_goods_sku set stock=new_stock,sales=new_sales where id=sku_id and stock=origin_stock
                    # 返回受影响的行数
                    res = GoodsSKU.objects.filter(id=sku_id, stock=origin_stock).update(stock=new_stock, sales=new_sales)
                    if not res:
                        if i == 2:  # 重复执行3次还没成功
                            transaction.savepoint_rollback(save_id)
                            return JsonResponse({'res': 7, 'errmsg': '下单失败2'})
                        continue

                    OrderGoods.objects.create(
                        order=order,
                        sku=sku,
                        count=count,
                        price=sku.price
                    )

                    # todo:累加计算订单商品的总数量和总价格
                    amount = sku.price * int(count)
                    total_count += int(count)
                    total_price += amount
                    break  # 执行成功跳出循环

            # todo:更新订单信息表中的总数量和总价格
            order.total_count = total_count
            order.total_price = total_price
            order.save()
        except:
            transaction.savepoint_rollback(save_id)
            return JsonResponse({'res': 7, 'errmsg': '下单失败'})

        # 提交事务
        transaction.savepoint_commit(save_id)

        # todo:清除用户购物车中对应的记录
        con.hdel(cart_key, *sku_ids)

        return JsonResponse({'res': 5, 'message': '添加成功'})


class OrderPayView(View):
    """订单支付"""
    def post(self, request):
        # 用户是否登录
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 0, 'errmsg': '请登陆'})

        # 接收参数
        order_id = request.POST.get('order_id')

        # 校验参数
        if not order_id:
            return JsonResponse({'res': 1, 'errmsg': '无效订单id'})
        try:
            order = OrderInfo.objects.get(
                order_id=order_id,
                user=user,
                pay_method=3,
                order_status=1
            )
        except OrderInfo.DoesNotExist:
            return JsonResponse({'res': 2, 'errmsg': '订单错误 '})

        # 业务处理：使用python sdk调用支付宝支付接口
        # 初始化
        alipay = AliPay(
            appid="2016101100658149",  # 应用id
            app_notify_url=None,  # 默认回调url
            app_private_key_path=os.path.join(settings.BASE_DIR, 'apps/order/app_private_key.pem'),
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_path=os.path.join(settings.BASE_DIR, 'apps/order/alipay_public_key.pem'),
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False,表示真实地址；True表示沙箱地址
        )

        # 调用支付接口
        # 电脑网站支付，需要跳转到https://openapi.alipaydev.com/gateway.do? + order_string
        total_pay = order.total_price + order.transit_price
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,  # 订单id
            total_amount=str(total_pay),  # 支付金额
            subject='天天生鲜%s' % order_id,
            return_url=None,
            notify_url=None  # 可选, 不填则使用默认notify url
        )

        # 返回应答
        pay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string

        return JsonResponse({'res': 3, 'pay_url': pay_url})


class OrderCheckView(View):
    """查询支付结果"""
    def post(self, request):
        # 用户是否登录
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 0, 'errmsg': '请登陆'})

        # 接收参数
        order_id = request.POST.get('order_id')

        # 校验参数
        if not order_id:
            return JsonResponse({'res': 1, 'errmsg': '无效订单id'})
        try:
            order = OrderInfo.objects.get(
                order_id=order_id,
                user=user,
                pay_method=3,
                order_status=1
            )
        except OrderInfo.DoesNotExist:
            return JsonResponse({'res': 2, 'errmsg': '订单错误 '})

        # 业务处理：使用python sdk调用支付宝支付接口
        # 初始化
        alipay = AliPay(
            appid="2016101100658149",  # 应用id
            app_notify_url=None,  # 默认回调url
            app_private_key_path=os.path.join(settings.BASE_DIR, 'apps/order/app_private_key.pem'),
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_path=os.path.join(settings.BASE_DIR, 'apps/order/alipay_public_key.pem'),
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False,表示真实地址；True表示沙箱地址
        )

        # 调用支付宝的交易查询接口
        while True:
            response = alipay.api_alipay_trade_query(order_id)

            # response = {
            #         "trade_no": "2017032121001004070200176844", # 支付宝交易号
            #         "code": "10000", # 接口调用是否成功
            #         "invoice_amount": "20.00",
            #         "open_id": "20880072506750308812798160715407",
            #         "fund_bill_list": [
            #             {
            #                 "amount": "20.00",
            #                 "fund_channel": "ALIPAYACCOUNT"
            #             }
            #         ],
            #         "buyer_logon_id": "csq***@sandbox.com",
            #         "send_pay_date": "2017-03-21 13:29:17",
            #         "receipt_amount": "20.00",
            #         "out_trade_no": "out_trade_no15",
            #         "buyer_pay_amount": "20.00",
            #         "buyer_user_id": "2088102169481075",
            #         "msg": "Success",
            #         "point_amount": "0.00",
            #         "trade_status": "TRADE_SUCCESS", # 支付结果
            #         "total_amount": "20.00"
            # }

            code = response.get('code')

            if code == '10000' and response.get('trade_status') == 'TRADE_SUCCESS':
                # 支付成功
                # 获取支付宝交易号
                trade_no = response.get('trade_no')
                # 更新订单状态
                order.trade_no = trade_no
                order.order_status = 4  # 待评价
                order.save()
                return JsonResponse({'res': 3, 'message': '支付成功'})

            elif code == '40004' or (code == '10000' and response.get('trade_status') == 'WAIT_BUYER_PAY'):
                # 业务失败，可能一会成功或等待买家付款
                import time
                time.sleep(5)
                continue
            else:
                return JsonResponse({'res': 4, 'errmsg': '支付失败'})


class OrderCommentView(LoginRequiredMixin, View):
    """订单评论"""
    def get(self, request, order_id):
        """提供评论页面"""
        user = request.user

        # 校验数据
        if not order_id:
            return redirect(reverse('user:order'))
        try:
            order = OrderInfo.objects.get(order_id=order_id, user=user)
        except OrderInfo.DoesNotExist:
            return redirect(reverse("user:order"))

        # 根据订单的状态获取订单的状态标题
        order.order_status_name = OrderInfo.ORDER_STATUS[order.order_status]

        # 获取订单商品信息
        order_skus = OrderGoods.objects.filter(order_id=order_id)
        for order_sku in order_skus:
            amount = order_sku.count*order_sku.price
            # 动态给order_sku增加属性amount,保存商品小计
            order_sku.amount = amount
        # 动态给order增加属性order_skus, 保存订单商品信息
        order.order_skus = order_skus

        return render(request, "order_comment.html", {"order": order})

    def post(self, request, order_id):
        """处理评论内容"""
        user = request.user
        # 校验数据
        if not order_id:
            return redirect(reverse('user:order'))
        try:
            order = OrderInfo.objects.get(order_id=order_id, user=user)
        except OrderInfo.DoesNotExist:
            return redirect(reverse("user:order"))

        # 获取评论条数
        total_count = request.POST.get("total_count")
        total_count = int(total_count)

        # 循环获取订单中商品的评论内容
        for i in range(1, total_count + 1):
            # 获取评论的商品的id
            sku_id = request.POST.get("sku_%d" % i)  # sku_1 sku_2
            # 获取评论的商品的内容
            content = request.POST.get('content_%d' % i, '')  # cotent_1 content_2 content_3
            try:
                order_goods = OrderGoods.objects.get(order=order, sku_id=sku_id)
            except OrderGoods.DoesNotExist:
                continue

            order_goods.comment = content
            order_goods.save()

        order.order_status = 5  # 已完成
        order.save()

        return redirect(reverse("user:order", kwargs={"page": 1}))
