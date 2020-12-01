from django.urls import path
from django.conf.urls import url, include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'classes'

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^view/', include('classes.view.urls')),
    url(r'^add/', include('classes.add.urls')),
    url(r'^drop/', include('classes.drop.urls')),
    
]

urlpatterns += staticfiles_urlpatterns()