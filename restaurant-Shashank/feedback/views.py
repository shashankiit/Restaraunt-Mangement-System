from django.shortcuts import render
from .models import *
from datetime import date, datetime, time
from django.shortcuts import redirect
# Create your views here.

def dispf(request,pnum):
    return render(request,"feedback/feedform.html")

def strindb(request,pnum):
    user = User.objects.get(phone = int(pnum))
    alldata = request.POST
    com = alldata["comment"]
    rate = alldata["rate"]
    fcom = Review.objects.create(user = user,comment = com,date = date.today(),rating = int(rate))
    fcom.save()
    return redirect('/')

