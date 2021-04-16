from django.urls import path
from django.urls import reverse
from . import views

urlpatterns = [
    path('<pnum>/order', views.itemlist, name='index'),
    
    # path('continue', views.cont, name = 'continue')
]