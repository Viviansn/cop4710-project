from django.urls import path
from django.conf.urls import url, include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'drop'

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^success/$', views.drop_success, name="drop_success"),
]

urlpatterns += staticfiles_urlpatterns()