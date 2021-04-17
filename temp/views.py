from functools import total_ordering
from django.shortcuts import render
# Create your views here.
from .models import *

def menu_item_list(request):
	allmenu = menu_items.objects.all()
	return render(request, 'automate/menu.html', {'menu':allmenu})

def conforder(request):
	if request.method == 'POST':
		alldata = request.POST
		quantity = alldata.getlist('Quantity')
		filter_object = filter(lambda x: x != "", quantity)
		quantity = list(filter_object)
		item = alldata.getlist('Checkbox')
		choices = menu_items.objects.filter(item_name__in=item)
		totalprice = 0
		empty=[]
		for i in range(len(item)):
			name = item[i]
			object=menu_items.objects.get(item_name=name)
			price=object.selling_price
			empty.append(price*int(quantity[i]))
			totalprice += price*int(quantity[i])
			# DO DISCOUNT HERE
			finalprice = totalprice
		mylist = zip(choices, quantity, empty)
		context = {'chosen':mylist ,'totprice':totalprice, 'finprice':finalprice}
	return render(request, 'automate/conford.html', context)