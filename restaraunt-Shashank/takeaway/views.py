from django.shortcuts import render
from userlog.models import User

# Create your views here.

def itemlist(request): # always get this page
    pnum = request.POST["pnum"]
    user = User.objects.get(phone = pnum)
    if user.area_code == None:
        return render(request,"dispdets.html",{"user":user})
    return render(request,"itemlist.html",{"user":user})