from reserve_tab.views import timeadd
from django.shortcuts import render
from .models import *
from django.shortcuts import redirect
from django.contrib import messages
from datetime import date, datetime, time

def menu_item_list(request,pnum):
	alltables = Dining_table.objects.filter(phone_occupied=int(pnum))
	allmenu = Menu_item.objects.all()
	user = User.objects.get(phone=int(pnum))
	if alltables.count() != 0:
		return render(request, 'accept_res/menu.html', {'menu':allmenu,"user":user})
	else:
		todate = date.today()
		nowtime = datetime.now().time()
		useres = Reservation.objects.filter(phone=int(pnum),date_for_res=todate).order_by('time_for_res')
		# mytableid = useres.order_by('time_for_res').first().table_id
		if useres.count() == 0:
			messages.info(request, "You don\'t have an existing reservation") 
			return redirect('/ufunc')
		else:
			#################
			mytableid = useres.order_by('time_for_res').first().table_id
			##################
			for i in range(useres.count()):
				stime = useres[i].time_for_res
				strtime = stime.strftime("%H:%M")
				after = timeadd(strtime,"00:30")
				start = after.split(':')
				after=time(hour=int(start[0]),minute=int(start[1]),second=0)
				if (nowtime < stime):
					##############################
					messages.info(request, f"You are early, please come after start of your slot {str(stime)} at {str(todate)}")
					##############################
					return redirect('/ufunc')
				elif (nowtime > after):
					messages.info(request, "You are late, your reservation is void")
					################## remove reservation (tested right)
					useres[i].delete()
					##################################
					return redirect('/ufunc')
				else:
					allt = Dining_table.objects.get(table_id=mytableid)
					allt.phone_occupied=int(pnum)
					allt.save()
					return render(request, 'accept_res/menu.html', {'menu':allmenu,"user":user})

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
		pnum=int(pnum)
		user= User.objects.get(phone=pnum)
		finalprice = totalprice -  int(user.loyalty.discount_perc*totalprice/100)
		user.mon_spent+=finalprice
		user.save()
		bud = Budget.objects.get(day=date.today())
		bud.earned+=finalprice
		bud.save()
		mylist = zip(choices, quantity, empty)
		context = {'chosen':mylist ,'totprice':totalprice, 'finprice':finalprice, 'pnum':pnum}
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
		nowtime = datetime.now().time()
		useres = Reservation.objects.filter(phone=int(pnum),date_for_res=todate)
		mytableid = useres.order_by('time_for_res').first().table_id
		useres[0].delete()
		tab = Dining_table.objects.get(table_id=mytableid)
		tab.phone_occupied = None
		tab.save()
		########################################
		return redirect('/ufunc') ## redirect to feedback