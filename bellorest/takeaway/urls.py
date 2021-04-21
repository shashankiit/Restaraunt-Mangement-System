from django.urls import path
from . import views

urlpatterns = [
    path('<pnum>/menu/', views.menu_item_list),
    path('<pnum>/menu/choices/', views.conforder),
    path('<pnum>/menu/choices/con/',views.feed)
]