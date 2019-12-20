from django.core.mail import send_mail
from django.conf import settings
from django.template import loader
from celery import Celery

# django环境的初始化
import os
# import django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dailyfresh.settings')
# django.setup()

from apps.goods.models import GoodsType, IndexGoodsBanner, IndexPromotionBanner, IndexTypeGoodsBanner


app = Celery('celery_tasks.tasks', broker='redis://:2017916yuan@127.0.0.1:6379/8')


@app.task
def send_register_active_email(to_email, username, token):
    """发送激活邮件"""
    subject = '天天生鲜欢迎信息'
    message = ''  # 邮件正文
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    html_message = '<h1>%s，欢迎您成为天天生鲜注册会员</h1>' \
                   '请点击链接激活您的账户<br/>' \
                   '<a href="http://127.0.0.1:8001/user/active/%s">' \
                   'http://127.0.0.1:8000/user/active/%s</a>' \
                   % (username, token, token)
    send_mail(subject, message, sender, receiver, html_message=html_message)


@app.task
def generate_static_index_html():
    """产生首页静态页面"""
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
    # 加载模板文件，返回模板对象
    temp = loader.get_template('static_index.html')
    # 模板渲染
    static_index_html = temp.render(context)
    # 生成首页对应静态文件
    save_path = os.path.join(settings.BASE_DIR, 'index.html')
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(static_index_html)

