from django.shortcuts import render
from userlog.models import User

# Create your views here.

def itemlist(request,pnum): # always get this page
    pnum = int(pnum)
    user = User.objects.get(phone = pnum)
    return render(request,"itemlist.html",{"user":user})