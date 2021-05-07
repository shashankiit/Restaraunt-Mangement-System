from django.shortcuts import render
from .models import *
from takeaway.models import *
from django.shortcuts import redirect
from django.contrib import messages
from datetime import date, datetime, time, timedelta
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
        user.loyaltyupdate()
        user.save()
    else:
        user = User.objects.create(phone = pnum,name = name,address = addr,area_code=arcode,mon_spent = 0,loyalty=Loyalty_level.objects.get(loyalty_points=0))
        user.save()
    inv = Inventory.objects.all()
    bud = Budget.objects.filter(day=date.today())
    if not bud.exists():
        bud = Budget.objects.create(day=date.today(),spent=0,earned=0)
        bud.save()
    bud = Budget.objects.get(day=date.today())
    for ingred in inv:
        if ingred.quantity < ingred.min_quantity :
            ingred.quantity+=ingred.min_quantity
            ingred.save()
            bud.spent+=ingred.min_quantity * ingred.cost_price
            bud.save()
    # tablephone = Dining_table.objects.get(phone_occupied)
    res = Reservation.objects.filter(date_for_res__lt=date.today())
    for i in res:
        i.delete()
    res = Reservation.objects.filter(date_for_res=date.today())
    for i in res:
        time1 = i.time_for_res.strftime("%H:%M")
        split1 = time1.split(":")
        seconds1 = int(split1[0])*3600 + int(split1[1])*60
        timenow1 = datetime.now().time().strftime("%H:%M")
        split1 = timenow1.split(":")
        seconds2 = int(split1[0])*3600 + int(split1[1])*60
        if(seconds2 - seconds1 > 1800):
            if(Dining_table.objects.filter(phone_occupied=i.phone).count() == 0):
                i.delete()
    return render(request,"userlog/dispoptions.html",{"user":user})

def takeaway(request):
    if request.method == "POST":
        pnum = request.POST["pnum"]
        user = User.objects.get(phone=pnum)
        if user.area_code == None:
            messages.info(request, 'No area code available')
            return redirect('/ufunc/')
        else:
            delev = Delivery_staff.objects.filter(area_code = user.area_code,available_stat=1)
            if delev.exists():
                return redirect('/takeaway/'+str(pnum)+'/'+str(delev[0].pk)+'/menu')
            else:
                messages.info(request, 'Our current active staff can\'t deliver to your area code')
                return redirect('/ufunc/')

def dinein(request):
    if request.method == "POST":
        pnum = request.POST["pnum"]
        return redirect('/dinein/'+str(pnum)+'/dinein')

def accres(request):
    if request.method == "POST":
        pnum = request.POST["pnum"]
        return redirect('/accept_res/'+str(pnum)+'/menu')

def restable(request):
    if request.method == "POST":
        pnum = request.POST["pnum"]
        return redirect('/reserve_tab/'+str(pnum)+'/reservation')