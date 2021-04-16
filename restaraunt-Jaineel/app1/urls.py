from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add1', views.add, name='add'),
    path('feedback', views.feedback, name='feedback')
]