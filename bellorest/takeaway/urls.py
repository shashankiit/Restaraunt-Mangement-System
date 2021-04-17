from django.urls import path
from . import views

urlpatterns = [
    path('<pnum>/menu/', views.menu_item_list),
    path('choices/', views.conforder),
]