"""sfmc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
#from django.contrib import admin
from demo import views

urlpatterns = [
    url(r'^test/$', views.IndexView.as_view(), name='index'),
    url(r'^sfmc/sign_in/$', views.SignInView.as_view(), name='sfmc.signin'),
    url(r'^sfmc/refresh_token/$', views.RefreshTokenView.as_view(), name='sfmc.refresh_token'),
    url(r'^fire/$', views.FireEventView.as_view(), name='fire'),
    url(r'^logs/$', views.LogView.as_view(), name='sfmc.logs'),
    url(r'^tokenContext/$', views.TokenContextView.as_view(), name='tokenContext'),
    url(r'^activity/(?P<action>[^/]+)/$', views.ActivityActionView.as_view(), name='activity.action'),
    url(r'^event/save/$', views.EventSaveView.as_view(), name='event.save'),
]
