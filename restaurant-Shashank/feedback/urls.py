from django.urls import path
from . import views

urlpatterns = [
    path('<pnum>/',views.dispf),
    path('<pnum>/strindb/',views.strindb)
]