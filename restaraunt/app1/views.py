from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request,'home.html',{"name":"Shashank"})

def add(request):
    v1 = request.POST['num1']
    v2 = request.POST['num2']
    r=int(v1)+int(v2)
    return render(request,'result.html',{'result':r})
