from django.conf.urls import re_path
from . import views

app_name = 'Tblog'

urlpatterns = [
    re_path(r'^$', views.index, name='blog_index'),
    re_path(r'^(?P<blog_id>[0-9]+)', views.detail, name='blog_detail'),
]