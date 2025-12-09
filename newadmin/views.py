from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from reviews.models import Reviewer
# Create your views here.

def register(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pswd = request.POST.get('pswd')
        user = User.objects.create_superuser(username=uname,password=pswd)
        return redirect('reg')
    return render(request,'newadmin/register.html')

data = [
        "SIYAHUDHEEN_FLUTTER",
        "IRSHAD_FLUTTER",
        "AKHIL_FLUTTER",
        "AJMAL_FLUTTER",
        "JASSIM_FLUTTER",
        "LIKHIN_FLUTTER",
        "JUSTINE_FLUTTER",
    ]

def addlist(request):
    Reviewer.objects.create(name=data,stack='FLUTTER')
    return render(request,'newadmin/test.html')