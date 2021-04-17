from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.menu_item_list),
    path('choicex/', views.conforder),
]