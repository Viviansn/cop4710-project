from django.urls import path
from django.conf.urls import url, include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'add'

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^results/$', views.results, name="results"),
    url(r'^success/$', views.add_success, name="add_success"),
]

urlpatterns += staticfiles_urlpatterns()