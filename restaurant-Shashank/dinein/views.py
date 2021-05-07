from django.shortcuts import redirect, render
from .models import *
from django.contrib import messages
from datetime import time, date, datetime

flag = 0

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

def reservation(request, pnum):
	user = User.objects.get(phone=int(pnum))
	todate = datetime.today().date()
	startime = datetime.today().time()
	return render(request, 'dinein/dinein.html', {"user":user, "todate":todate, "curtime":startime})

def confres(request, pnum):
	if request.method == 'POST':
		alldata = request.POST
		lister = alldata.getlist('name')
		restime = alldata["nowtime"]
		diners = lister[0]
		date = datetime.today().date()
		time = datetime.today().time().strftime("%H:%M")
		tdur = lister[1]
		endtime = timeadd(time, tdur)
		context = {'diners':diners ,'date':date, 'restime':time, 'duration':tdur, 'endtime':endtime, 'user':pnum}
	return render(request, 'dinein/confres.html', context)

def buttonform(request, pnum):
	tablers = Dining_table.objects.filter(phone_occupied=int(pnum))
	if tablers.count() == 1:
		curres = Reservation.objects.get(phone=int(pnum),table_id=tablers.first().table_id)
		sttime = curres.time_for_res
		tdtime = curres.reservation_duration
		entime = timeadd(str(sttime),str(tdtime))
		split = entime.split(':')
		now = datetime.now()
		resend = datetime(now.year,now.month,now.day,int(split[0]),int(split[1]))
		delta = resend - now
		allmenu = Menu_item.objects.all()
		user = User.objects.get(phone=int(pnum))
		#############pass time
		timeleft = int(delta.total_seconds())
		topit = Menu_item.objects.all().order_by('-order_frequency')
		a=min(len(topit),5)
		topit = topit[:a]
		return render(request, 'dinein/menu.html', {'menu':allmenu,"user":user,"tleft":timeleft,"topit":topit})
	if request.POST["action"] == "Confirm" and (tablers.count() == 0):
		# GRAB DATA FROM URL
		diners = int(request.POST["diners"])
		restime = request.POST["restime"]
		timedur = request.POST["duration"]
		endtime = request.POST["endtime"]
		# FORMAT DATA FOR COMPARISON
		start = restime.split(':')
		timeup=time(hour=int(start[0]),minute=int(start[1])) # diner starttime datetime class
		start = endtime.split(':')
		timedown=time(hour=int(start[0]),minute=int(start[1])) # diner endtime datetime class
		today = date.today()
		# START COMPUTATION
		dateres = Reservation.objects.filter(date_for_res=today)
		occupied_tables=[]
		occupied_objects=[]
		for i in range(dateres.count()):
			current = dateres[i] # Res object
			stime = current.time_for_res # Start of res datetime class
			sdur = stime.strftime('%H:%M') # start of res in string
			tdur = current.reservation_duration.strftime('%H:%M') # duration of res in string
			etime = timeadd(tdur,sdur) # endtime in string
			start = endtime.split(':')
			etime=time(hour=int(start[0]),minute=int(start[1])) # endtime in datetime class
			overlapval = overlap(stime,etime,timeup,timedown)
			if overlapval == True:
				occupied_tables.append(int(current.table_id))
				occupied_objects.append(current)
			else:
				continue
		alltables = Dining_table.objects.filter(capacity__gte=diners, phone_occupied=None)
		alltab=[]
		for i in range(alltables.count()):
			alltab.append(int(alltables[i].table_id))
		avaitables = differlist(alltab,occupied_tables)
		print(avaitables)
		blocked_slots_list = []
		for i in range(len(occupied_objects)):
			stime = occupied_objects[i].time_for_res.strftime('%H:%M')
			tdur = occupied_objects[i].reservation_duration.strftime('%H:%M')
			etime = timeadd(tdur,sdur)
			stringer = stime + ' - ' + etime
			blocked_slots_list.append(stringer)
		if len(avaitables)==0:
			messages.info(request, 'No Tables Available till that time')
			return redirect('/dinein/'+str(pnum)+'/dinein')
		# GET TABLE OBJECTS WHICH ARE AVAILABLE
		avaitobj = Dining_table.objects.filter(table_id__in=avaitables)
		avaitsobj = avaitobj.order_by('capacity').first()
		mytableid = avaitsobj.table_id
		Reservation.objects.create(table_id=mytableid,phone = pnum,date_for_res=today,num_diners=diners,time_for_res=timeup,reservation_duration=timedur)
		allt = Dining_table.objects.get(table_id=mytableid)
		allt.phone_occupied=int(pnum)
		allt.save()
		messages.info(request, 'Have a nice meal')
		allmenu = Menu_item.objects.all()
		user = User.objects.get(phone=int(pnum))
		#### pass time
		split = str(timedur).split(':')
		tleft = int(split[0])*3600 + int(split[1])*60
		topit = Menu_item.objects.all().order_by('-order_frequency')
		a=min(len(topit),5)
		topit = topit[:a]
		return render(request, 'dinein/menu.html', {'menu':allmenu,"user":user,"tleft":tleft,"topit":topit})
	else:
		messages.info(request, 'Try adjusting time')
		return redirect('/dinein/'+str(pnum)+'/dinein/')

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
				return redirect('/dinein/'+str(pnum)+'/dinein/confirmation/update/')
			price=object1.selling_price
			empty.append(price*int(quantity[i]))
			totalprice += price*int(quantity[i])
		for i in range(len(item)):
			name = item[i]
			object1 = Menu_item.objects.get(item_name=name)
			object1.order_frequency+=int(quantity[i])
			object1.save()
		pnum=int(pnum)
		user= User.objects.get(phone=pnum)
		finalprice = totalprice -  int(user.loyalty.discount_perc*totalprice/100)
		user.mon_spent+=finalprice
		user.save()
		bud = Budget.objects.get(day=date.today())
		bud.earned+=finalprice
		bud.save()
		mylist = zip(choices, quantity, empty)
		######## pass time
		tablers = Dining_table.objects.filter(phone_occupied=int(pnum))
		curres = Reservation.objects.get(phone=int(pnum),table_id=tablers.first().table_id)
		sttime = curres.time_for_res
		tdtime = curres.reservation_duration
		entime = timeadd(str(sttime),str(tdtime))
		split = entime.split(':')
		now = datetime.now()
		resend = datetime(now.year,now.month,now.day,int(split[0]),int(split[1]))
		delta = resend - now
		tleft = int(delta.total_seconds())
		context = {'chosen':mylist ,'totprice':totalprice, 'finprice':finalprice, 'user':user,"tleft":tleft}
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
		return redirect('/dinein/'+str(pnum)+'/dinein/confirmation/update/')
	else:
		# SET PHONE NUMBER in Dining_table TO NULL
		todate = date.today()
		useres = Reservation.objects.filter(phone=int(pnum),date_for_res=todate)
		mytableid = useres.order_by('time_for_res').first().table_id
		useres[0].delete()
		tab = Dining_table.objects.get(table_id=mytableid)
		tab.phone_occupied = None
		tab.save()
		return redirect(f"/feedback/{pnum}")