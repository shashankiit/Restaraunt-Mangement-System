from django.shortcuts import render
from django.shortcuts import redirect
# Create your views here.
def dispop(request):
    return render(request,'startpage/dispoptions.html')


def dec(request):
    res = request.POST["action"]
    if res == "Admin":
        return redirect("/admin")
    else:
        return redirect("/ufunc")