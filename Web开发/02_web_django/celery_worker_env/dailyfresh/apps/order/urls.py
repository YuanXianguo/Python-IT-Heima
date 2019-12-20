from django.conf.urls import url
from apps.order import views

urlpatterns = [
    url(r'^place$', views.OrderPlaceView.as_view(), name='place'),
    url(r'^commit$', views.OrderCommitView.as_view(), name='commit'),
    url(r'^pay$', views.OrderPayView.as_view(), name='pay'),
    url(r'^check$', views.OrderCheckView.as_view(), name='check'),
    url(r'^comment/(?P<order_id>.+)$', views.OrderCommentView.as_view(), name='comment')
]
