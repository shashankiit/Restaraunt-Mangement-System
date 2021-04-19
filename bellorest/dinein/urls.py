from django.urls import path
from . import views

urlpatterns = [
    path('<pnum>/dinein/', views.reservation),
    path('<pnum>/dinein/confirmation/', views.confres),
    path('<pnum>/dinein/confirmation/update/', views.buttonform),
    path('<pnum>/dinein/confirmation/update/confirm/', views.conforder),
    path('<pnum>/dinein/confirmation/update/confirm/orderagain/', views.orderagain),
]