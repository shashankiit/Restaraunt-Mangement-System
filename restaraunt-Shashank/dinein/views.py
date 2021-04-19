from django.shortcuts import render,redirect
from userlog.models import *
from takeaway.models import *
from reserve_tab.models import *
from datetime import time, date, datetime
from django.contrib import messages
# Create your views here.

# def itemlist(request,pnum): # always get this page
#     pnum = int(pnum)
#     user = User.objects.get(phone = pnum)
#     return render(request,"itemlist.html",{"user":user})

def dnin(request,pnum):
	user = User.objects.get(phone=int(pnum))
	return render(request, 'dinein/inputdets.html', {"user":user})

# *********************************************
def differlist(li1, li2):
	setA=set(li1)
	setB=set(li2)
	return list(setA.difference(setB))

def overlap(s1, e1, s2, e2):
	return not (e2 < s1 or e1 < s2)

def timeadd(t1,t2):
	t1l = t1.split(':')
	t2l = t2.split(':')
	minute = 0
	hour = 0
	minute = int(t1l[1]) + int(t2l[1])
	while minute >= 60:
		hour +=1
		minute -= 60
	hour += int(t1l[0]) + int(t2l[0])
	if minute < 10:
		minute = "0" + str(minute)
	time = str(hour) + ":" + str(minute)
	return time
# **************************************************
def confres(request,pnum):
	user = User.objects.get(phone=int(pnum))
	alldata = request.POST
	timedur = alldata["tdur"]
	diners = int(alldata["numd"])
	datex = date.today()
	restime = datetime.now().strftime("%H:%M")
	endtime = timeadd(restime,timedur)


	start = restime.split(':')
	timeup=time(hour=int(start[0]),minute=int(start[1]),second=0)
	start = endtime.split(':')
	timedown=time(hour=int(start[0]),minute=int(start[1]),second=0)
	start = datex.split('-')
	datex = date(year=int(start[0]),month=int(start[1]),day=int(start[2]))
	today = date.today()
	#logic for tables

	dateres = Reservation.objects.filter(date_for_res=datex)
	occupied_tables=[]
	occupied_objects=[]

	for i in range(dateres.count()):
		current = dateres[i]
		stime = current.time_for_res
		sdur = stime.strftime('%H:%M')
		tdur = current.reservation_duration.strftime('%H:%M')
		etime = timeadd(tdur,sdur)
		start = endtime.split(':')
		etime=time(hour=int(start[0]),minute=int(start[1]),second=0)
		overlapval = overlap(stime,etime,timeup,timedown)
		if overlapval == True:
			occupied_tables.append(int(current.table_id))
			occupied_objects.append(current)
		else:
			continue
	
	alltables = Dining_table.objects.filter(capacity__gte=diners)
	alltab=[]
	for i in range(alltables.count()):
		alltab.append(int(alltables[i].table_id))
	avaitables = differlist(alltab,occupied_tables)
	blocked_slots_list = []
	for i in range(len(occupied_objects)):
		stime = occupied_objects[i].time_for_res.strftime('%H:%M')
		tdur = occupied_objects[i].reservation_duration.strftime('%H:%M')
		etime = timeadd(tdur,sdur)
		stringer = stime + ' - ' + etime
		blocked_slots_list.append(stringer)
	if len(avaitables)==0:
		# Ask to wait in queue
		# get the last slot table
		messages.info(request, 'No Tables Available at that time')
		context = {"user":user,"table":tabid,"tdur":timedur,"numd":diners} 
		return render(request,"dinein/dineinop.html",context)

	# GET TABLE OBJECTS WHICH ARE AVAILABLE
	avaitobj = Dining_table.objects.filter(table_id__in=avaitables)
	avaitsobj = avaitobj.order_by('capacity').first()
	mytableid = avaitsobj.table_id
	Reservation.objects.create(table_id=mytableid,phone = pnum,date_for_res=datex,num_diners=diners,time_for_res=timeup,reservation_duration=timedur)

def update(request):
	if request.POST["decision"] == "Yes":
		alldata = request.POST
		mytableid = alldata["tbid"]
		pnum = int(alldata["pnum"])


		timedur = alldata["tdur"]
		diners = int(alldata["numd"])
		datex = date.today()
		restime = datetime.now().strftime("%H:%M")
		endtime = timeadd(restime,timedur)


		start = restime.split(':')
		timeup=time(hour=int(start[0]),minute=int(start[1]),second=0)
		start = endtime.split(':')
		timedown=time(hour=int(start[0]),minute=int(start[1]),second=0)
		start = datex.split('-')
		datex = date(year=int(start[0]),month=int(start[1]),day=int(start[2]))
		today = date.today()


		restime = datetime.now().strftime("%H:%M")
		Reservation.objects.create(table_id=mytableid,phone = pnum,date_for_res=date.today(),num_diners=diners,time_for_res=timeup,reservation_duration=timedur)
		context = {}
		return render(request,"dinein/dineinwait.html",context)
	else:
		pass


def menu_item_list(request,pnum):
	allmenu = Menu_item.objects.all()
	user = User.objects.get(phone=int(pnum))
	todate = date.today()
	nowtime = datetime.now().time()
	useres = Reservation.objects.filter(phone=int(pnum),date_for_res=todate)
	if useres.count() == 0:
		messages.info(request, "You don\'t have an existing reservation")
		return redirect('/ufunc')
	else:
		for i in range(useres.count()):
			stime = useres[i].time_for_res
			strtime = stime.strftime("%H:%M")
			after = timeadd(strtime,"00:30")
			start = after.split(':')
			after=time(hour=int(start[0]),minute=int(start[1]),second=0)
			if (nowtime < stime):
				messages.info(request, "You are early, please come after start of your slot")
				return redirect('/ufunc')
			elif (nowtime > after):
				messages.info(request, "You are late, your reservation is void")
				return redirect('/ufunc')
			else:
				return render(request, 'dinein/menu.html', {'menu':allmenu,"user":user})



def trytoenter(request):
	alldata = request.POST
	if alldata["action"]=="Enter":
		#check if reservation is appropriate from acceptres
		return menu_item_list(request,alldata["pnum"])
	else:
		return redirect("/ufunc")
		# go back to ufunc



def conforder(request,pnum):
	if request.method == 'POST':
		alldata = request.POST
		pnum = alldata["pnum"]
		quantity = alldata.getlist('Quantity')
		filter_object = filter(lambda x: x != "", quantity)
		quantity = list(filter_object)
		item = alldata.getlist('Checkbox')
		choices = Menu_item.objects.filter(item_name__in=item)
		totalprice = 0
		finalprice = 0
		empty=[]
		ling={}
		#checking if ingredient available
		for i in range(len(item)):
			name = item[i]
			object1=Menu_item.objects.get(item_name=name)
			ling,check=chekifavail(object1,quantity[i],ling)
			if (not check):
				#message and redirect to item list
				restoreing(ling)
				messages.info(request, f'Ingredients not available for {object1.item_name}')
				return redirect('/dinein/'+str(pnum)+'/menu')
			price=object1.selling_price
			empty.append(price*int(quantity[i]))
			totalprice += price*int(quantity[i])
		pnum=int(pnum)
		user= User.objects.get(phone=pnum)
		loyal = user.loyalty
		loyal = Loyalty_level.objects.get(loyalty_points=loyal)
		finalprice = totalprice -  int(loyal.discount_perc*totalprice/100)
		user.mon_spent+=finalprice
		user.save()
		bud = Budget.objects.get(day=date.today())
		bud.earned+=finalprice
		bud.save()
		mylist = zip(choices, quantity, empty)
		context = {'chosen':mylist ,'totprice':totalprice, 'finprice':finalprice, 'pnum':pnum}
	return render(request, 'dinein/conford.html', context)

def chekifavail(item,quantity,ling):
	listofingred = item.getingred()
	for item_ingred in listofingred:
		ing = item_ingred.ingredient
		if ing.ingredient_name not in ling:
			ling[ing.ingredient_name]=ing.quantity
		usage = item_ingred.use_quantity * int(quantity)
		quantity_available = ing.quantity
		if(usage > quantity_available):
			return ling,False
		ing.quantity = ing.quantity - usage
		ing.save()

	return ling,True

def restoreing(ling):
	for ing_name in ling:
		ing = Inventory.objects.get(ingredient_name=ing_name)
		ing.quantity = ling[ing_name]
		ing.save()

def orderagain(request, pnum):
	if request.POST["action"] == "Order More":
		return redirect('/dinein/'+str(pnum)+'/menu')
	else:
		return redirect('/ufunc')
