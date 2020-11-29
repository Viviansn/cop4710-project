from django.urls import path
from django.conf.urls import url, include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'view'

urlpatterns = [
    url(r'^$', views.home, name="home"),
]

urlpatterns += staticfiles_urlpatterns()