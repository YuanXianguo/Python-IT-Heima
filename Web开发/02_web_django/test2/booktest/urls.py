from django.conf.urls import url
from booktest import views


urlpatterns = [
    url(r'^index$', views.index, name='index'),
    url(r'^create$', views.create),
    url(r'^delete/(\d+)$', views.delete),
    url(r'^ajax_test$', views.ajax_test),  # 显示ajax页面
    url(r'^ajax_handle$', views.ajax_handle),  # 处理ajax页面
    url(r'^ajax_login$', views.ajax_login),
    url(r'^ajax_login_check$', views.ajax_login_check),
    url(r'^set_cookie$', views.set_cookie),
    url(r'^get_cookie$', views.get_cookie),
    url(r'^set_session$', views.set_session),
    url(r'^get_session$', views.get_session),
    url(r'^url_reverse$', views.url_reverse),
    url(r'^show_args/(\d+)/(\d+)$', views.show_args, name='show_args'),
    url(r'^show_kwargs/(?P<c>\d+)/(?P<d>\d+)$', views.show_args, name='show_kwargs'),
    url(r'^redirect_reverse$', views.redirect_reverse),

]
