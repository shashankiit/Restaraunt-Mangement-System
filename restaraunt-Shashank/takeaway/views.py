from django.shortcuts import render
from .models import *
from django.shortcuts import redirect
from django.contrib import messages
from datetime import date
from background_task import background
# Create your views here.

def menu_item_list(request,pnum,delid):
	allmenu = Menu_item.objects.all()
	user = User.objects.get(phone=int(pnum))
	return render(request, 'takeaway/menu.html', {'menu':allmenu,"user":user})

def conforder(request,pnum,delid):
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
				messages.info(request, f'Ingredient not available for {object1.item_name}')
				# return redirect('/takeaway/'+str(pnum)+'/menu')
				return redirect('/takeaway/'+str(pnum)+'/'+str(delid)+'/menu')
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
		finalprice = totalprice - int(user.loyalty.discount_perc*totalprice/100)
		user.mon_spent+=finalprice
		user.save()
		bud = Budget.objects.get(day=date.today())
		bud.earned+=finalprice
		bud.save()
		mylist = zip(choices, quantity, empty)
		########################################### to add return of delivery staff code
		deliv = Delivery_staff.objects.get(pk = int(delid))
		deliv.available_stat = 0
		deliv.save()
		reset_del(int(delid))
		#########################################
		context = {'chosen':mylist ,'totprice':totalprice, 'finprice':finalprice, 'user':user, 'deliv':deliv}
	return render(request, 'takeaway/conford.html', context)

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

def feed(request,pnum,delid):
	return redirect(f"/feedback/{pnum}") ## redirect to feedback


@background(schedule=10)
def reset_del(delid):
	# print('Yay')
	deliv = Delivery_staff.objects.get(pk = int(delid))
	deliv.available_stat = 1
	deliv.save()
	