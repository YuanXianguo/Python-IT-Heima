from django.conf.urls import url

from apps.user.views import RegisterView, ActiveView, LoginView, UserInfoView, UserOrderView, UserSiteView, LogoutView

urlpatterns = [
    # url(r'^register$', views.register, name='register'),
    url(r'^register$', RegisterView.as_view(), name='register'),
    url(r'^active/(?P<token>.*)$', ActiveView.as_view(), name='active'),
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),
    url(r'^order/(?P<page>\d+)$', UserOrderView.as_view(), name='order'),
    url(r'^site$', UserSiteView.as_view(), name='site'),
    url(r'^$', UserInfoView.as_view(), name='user'),
]
