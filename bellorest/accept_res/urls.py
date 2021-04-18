from django.urls import path
from . import views

urlpatterns = [
    path('<pnum>/menu/', views.menu_item_list),
    path('<pnum>/menu/confirm/', views.conforder),
    path('<pnum>/menu/confirm/orderagain/', views.orderagain),
]