from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^index/$', views.index, name='index'),  # 主页
    url(r'^login/$', views.login),  # 登录页
    url(r'^login_check/$', views.login_check),  # 登录验证页
    url(r'^add_new/$', views.add_new, name='add_new'),  # 添加新内容
    url(r'^find_all/$', views.find_all),  # 查询所有内容
    url(r'^find_query', views.find_query),  # 按照条件查询
    url(r'^$', views.index),  # 主页
]
