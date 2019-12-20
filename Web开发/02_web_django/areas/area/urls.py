from django.conf.urls import url
from area import views


urlpatterns = [
    url(r'^index$', views.index, name='index'),
    url(r'^upload_pic$', views.upload_pic),
    url(r'^upload_handle$', views.upload_handle),
    url(r'^show_area/(\d*)$', views.show_area),
    url(r'^areas$', views.areas),
    url(r'^prov$', views.prov),
    url(r'^city(\d+)$', views.city),
    url(r'^dis(\d+)$', views.city),
]
