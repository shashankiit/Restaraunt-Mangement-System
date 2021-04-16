from django.urls import path

from . import views

urlpatterns = [
    path('', views.entpno, name='index'),
    path('pnenter', views.pnentered, name = 'srchpnum'),
    path('update', views.update, name = 'update'),
    path('takeaway',views.takeaway,name = 'takeaway'),
    path('dinein',views.dinein,name = 'dinein'),
    path('accres',views.accres,name = 'accres'),
    path('restable',views.restable,name = 'restable')    
    # path('continue', views.cont, name = 'continue')
]