from django.urls import path, re_path
from . import views

urlpatterns = [
    # 主页，实参name，将这个URL模式的名称指定为index，让我们能够在代码的其他地方引用它；
    # 每当需要提供到这个主页的链接时，我们都将使用这个名称，而不是编写URL；
    path('', views.index, name='index'),
    # 显示所有的主题
    path('topics/', views.topics, name='topics'),
    # 特定主题的详细页面
    re_path(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),
    path('new_topic/', views.new_topic, name='new_topic'),
    re_path(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry, name='new_entry'),
    re_path(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name='edit_entry'),
]
