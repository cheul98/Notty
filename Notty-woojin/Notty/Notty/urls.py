"""Notty URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import NottyApp.views
from NottyApp.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',NottyApp.views.home, name='home'),
    path('setting/',NottyApp.views.setting, name='setting'),
    path('detail/',NottyApp.views.detail, name='detail'),
    path('favorite/',NottyApp.views.favorite, name='favorite'),
    path('sht_path/' ,NottyApp.views.sht_path, name='sht_path'),
    path('min_detail/' ,NottyApp.views.min_detail, name='min_detail'),
    path('sht_detail/',NottyApp.views.sht_detail, name='sht_detail'),
    path('sht/',NottyApp.views.sht, name='sht'),
    path('real_min/',NottyApp.views.real_min, name='real_min'),

    path('flash/',NottyApp.views.flash, name='flash'),
    path('arrive/',NottyApp.views.arrive, name='arrive'),
    
    path('firebase-messaging-sw.js', showFirebaseJS, name="show_firebase_js"),
    path('firebase-messaging-sw.js', showFirebaseJS2, name="show_firebase_js2"),
    path('send/' , send),

    
]
