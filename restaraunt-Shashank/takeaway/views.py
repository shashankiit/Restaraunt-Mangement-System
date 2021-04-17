from django.shortcuts import render
from userlog.models import User
from .models import *
# Create your views here.

# def itemlist(request,pnum): # always get this page
# 	pnum = int(pnum)
# 	user = User.objects.get(phone = pnum)

# 	return render(request,"itemlist.html",{"user":user})

def menu_item_list(request,pnum):
	allmenu = Menu_item.objects.all()
	user = User.objects.get(phone=int(pnum))
	return render(request, 'takeaway/menu.html', {'menu':allmenu,"user":user})

def conforder(request):
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
		for i in range(len(item)):
			name = item[i]
			object=Menu_item.objects.get(item_name=name)
			price=object.selling_price
			empty.append(price*int(quantity[i]))
			totalprice += price*int(quantity[i])
			# DO DISCOUNT HERE
			finalprice = totalprice
		mylist = zip(choices, quantity, empty)
		context = {'chosen':mylist ,'totprice':totalprice, 'finprice':finalprice, 'pnum':pnum}
	return render(request, 'takeaway/conford.html', context)