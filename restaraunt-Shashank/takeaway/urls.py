from django.urls import path
from django.urls import reverse
from . import views

urlpatterns = [
    # path('<pnum>/order', views.itemlist, name='index'),
    path('<pnum>/menu/', views.menu_item_list),
    path('choices/', views.conforder),
    # path('continue', views.cont, name = 'continue')
]