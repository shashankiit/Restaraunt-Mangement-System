from django.shortcuts import render
from django.http import HttpResponse
from app1 import models

# Create your views here.
def index(request):
    return render(request,'home.html',{"name":"Shashank"})

def add(request):
    v1 = request.POST['num1']
    v2 = request.POST['num2']
    r=int(v1)+int(v2)
    return render(request,'result.html',{'result':r})

def feedback(request):
    # v1 = request.POST['rate1']
    
    v1 = request.POST.get('rate1', False)
    v2 = request.POST.get('rate2', False)
    v3 = request.POST.get('rate3', False)
    v4 = request.POST.get('rate4', False)
    v5 = request.POST.get('rate5', False)
    comment = request.POST.get('comment', False)
    phone = request.POST.get('phone', False)
    date = request.POST.get('date', False)
    rating = 0
    if v1 == "on":
        rating = 1
    if v2 == "on":
        rating = 2
    if v3 == "on":
        rating = 3
    if v4 == "on":
        rating = 4
    if v5 == "on":
        rating = 5
    if request.method == "POST":
        print("This is post")
        # print(v1,v2,v3,v4,v5)
        print(phone, date, comment, rating)
        # print("This is post")
        ins = models.review(phone = phone, date = date, comment = comment, rating = rating)
        ins.save()
        print("The data has been save in DB")

    return render(request,'final.html', {})