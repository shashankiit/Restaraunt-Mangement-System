from reserve_tab.views import timeadd
from django.shortcuts import render
from .models import *
from django.shortcuts import redirect
from django.contrib import messages
from datetime import date, datetime, timedelta

def menu_item_list(request,pnum):
	alltables = Dining_table.objects.filter(phone_occupied=int(pnum))
	allmenu = Menu_item.objects.all()
	user = User.objects.get(phone=int(pnum))
	if alltables.count() != 0:
		return render(request, 'accept_res/menu.html', {'menu':allmenu,"user":user})
	else:
		nowtime = datetime.now()
		date_time = nowtime.strftime("%Y/%m/%d")
		datesplit = date_time.split("/")
		todate = date(int(datesplit[0]),int(datesplit[1]),int(datesplit[2]))
		useres = Reservation.objects.filter(phone=int(pnum),date_for_res=todate)
		todelete=[]
		if useres.count() == 0:
			messages.info(request, "You don\'t have an existing reservation") 
			return redirect('/ufunc')
		else:
			for i in range(useres.count()):
				stime = useres[i].time_for_res
				strtime = stime.strftime("%H:%M")
				start = strtime.split(':')
				stime = datetime(year=int(datesplit[0]),month=int(datesplit[1]),day=int(datesplit[2]),hour=int(start[0]),minute=int(start[1]))
				atime = stime + timedelta(minutes=30)
				btime = stime - timedelta(minutes=30)
				if nowtime > atime:
					todelete.append(useres[i])
					continue
				if (nowtime - stime < timedelta(hours=1)) or (stime - nowtime < timedelta(hours=1)):
					validres = True
					break
				else:
					continue
		for i in todelete:
			i.delete()	
		if (nowtime < btime):
			##############################
			messages.info(request, f"You are early, please come after start of your slot {str(stime)}")
			##############################
			return redirect('/ufunc')
		elif (nowtime > atime):
			messages.info(request, "You are late, your reservation is void")
			################## remove reservation (tested right)
			# useres[i].delete()
			##################################
			return redirect('/ufunc')
		elif validres and nowtime <= atime and nowtime >= stime:
			allt = Dining_table.objects.get(table_id=useres[i].table_id)
			allt.phone_occupied=int(pnum)
			allt.save()
			return render(request, 'accept_res/menu.html', {'menu':allmenu,"user":user})
		else:
			messages.info(request, f"There is no reservation or you haven't arrived on time")
			return redirect('/ufunc')

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
				return redirect('/accept_res/'+str(pnum)+'/menu')
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
		context = {'chosen':mylist ,'totprice':totalprice, 'finprice':finalprice, 'user':user}
	return render(request, 'accept_res/conford.html', context)

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
		return redirect('/accept_res/'+str(pnum)+'/menu')
	else:
		#### remove reservation and clear table (tested right)
		todate = date.today()
		useres = Reservation.objects.filter(phone=int(pnum),date_for_res=todate)
		ongoingres = useres.order_by('time_for_res').first()
		ongoingres.delete()
		tab = Dining_table.objects.get(phone_occupied=int(pnum))
		tab.phone_occupied = None
		tab.save()
		########################################
		return redirect(f"/feedback/{pnum}") ## redirect to feedback