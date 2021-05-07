from django.urls import path
from . import views

urlpatterns = [
    path('<pnum>/reservation/', views.reservation),
    path('<pnum>/reservation/confirmation/', views.confres),
    path('<pnum>/reservation/confirmation/update/', views.buttonform),
]