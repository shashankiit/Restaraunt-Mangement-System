from django.urls import path
from django.urls import reverse
from . import views

urlpatterns = [
    path('', views.itemlist, name='index'),
    
    # path('continue', views.cont, name = 'continue')
]