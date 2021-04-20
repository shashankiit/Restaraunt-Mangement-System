"""bellorest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include

urlpatterns = [
    path('',include('startpage.urls')),
    path('takeaway/',include('takeaway.urls')),
    path('ufunc/',include('userlog.urls')),
    path('dinein/',include('dinein.urls')),
    path('accept_res/',include('accept_res.urls')),
    path('reserve_tab/',include('reserve_tab.urls')),
    path('feedback/',include('feedback.urls')),
    path('admin/', admin.site.urls),
]
