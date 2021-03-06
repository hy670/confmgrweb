"""confmgrweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from confmgrweb.views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^head.html', head, name='head'),
    url(r'^left.html', left, name='left'),
    url(r'^main.html', main, name='main'),
    url(r'^tab.html', tab, name='tab'),
    url(r'^policytab.html', policytab, name='policytab'),
    url(r'^repolicytab.html', repolicytab, name='repolicytab'),
    url(r'^policysearch.html', policysearch, name='policysearch'),
    url(r'^policyzmbie.html', policyzmbie, name='policyzmbie'),

]
