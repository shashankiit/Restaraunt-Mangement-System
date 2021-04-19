from django.urls import path
from django.urls import reverse
from . import views

urlpatterns = [
    path('<pnum>/dinein', views.dnin, name='reserve_for_dinein'),
    path('<pnum>/dinein/check/', views.confres),
    path('<pnum>/dinein/check/update' , views.update),
    path('<pnum>/dinein/trytoenter' , views.trytoenter)
    # path('continue', views.cont, name = 'continue')
]