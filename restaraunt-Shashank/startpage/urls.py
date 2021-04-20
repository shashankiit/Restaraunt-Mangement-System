from django.urls import path
from . import views

urlpatterns = [
    path('', views.dispop, name='index'),
    path('mode',views.dec, name = 'mode')
]