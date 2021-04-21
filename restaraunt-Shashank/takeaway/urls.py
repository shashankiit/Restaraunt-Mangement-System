from django.urls import path
from . import views

urlpatterns = [
    path('<pnum>/<delid>/menu/', views.menu_item_list),
    path('<pnum>/<delid>/menu/choices/', views.conforder),
    path('<pnum>/<delid>/menu/choices/con/',views.feed)
]