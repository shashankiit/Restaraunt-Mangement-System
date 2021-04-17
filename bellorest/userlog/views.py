from django.shortcuts import render
from .models import *
from django.shortcuts import redirect
from django.contrib import messages
# Create your views here.

def entpno(request):
    return render(request,"userlog/enterphone.html")

def pnentered(request):
    num = request.POST["pnum"]
    num = int(num)
    user = User.objects.filter(phone = num)
    found = 0
    if user.exists():
        user = User.objects.get(phone = num)
        found = 1
    return render(request,"userlog/displaydets.html",{"found":found,"phone":num,"user":user})

def update(request):
    pnum = request.POST["pnum"]
    name = request.POST["name"]
    addr = request.POST["addr"]
    arcode = request.POST["arcode"]
    if arcode == '':
        arcode=None
    user = User.objects.filter(phone = pnum)
    if user.exists():
        user = User.objects.get(phone = pnum)
        user.phone = pnum
        user.name  = name
        user.address = addr
        user.area_code = arcode
        user.save()
    else:
        user = User.objects.create(phone = pnum,name = name,address = addr,area_code=arcode,mon_spent = 0,loyalty=0)
        user.save()
    return render(request,"userlog/dispoptions.html",{"user":user})

def takeaway(request):
    if request.method == "POST":
        pnum = request.POST["pnum"]
        user = User.objects.get(phone=pnum)
        if user.area_code == None:
            messages.info(request, 'No area code available')
            return redirect('/ufunc/')
        else:
            delev = Delivery_staff.objects.filter(area_code = user.area_code)
            if delev.exists():
                return redirect('/takeaway/'+str(pnum)+'/menu')
            else:
                messages.info(request, 'Delivery staff no code')
                return redirect('/ufunc/')

def dinein(request):
    if request.method == "POST":
        pnum = request.POST["pnum"]
        return redirect('/dinein/'+str(pnum)+'/order')

def accres(request):
    if request.method == "POST":
        pnum = request.POST["pnum"]
        return redirect('/accept_res/'+str(pnum)+'/order')

def restable(request):
    if request.method == "POST":
        pnum = request.POST["pnum"]
        return redirect('/reserve_tab/'+str(pnum)+'/order')