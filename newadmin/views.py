from django.shortcuts import render,redirect
from django.contrib.auth.models import User
# Create your views here.

def register(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pswd = request.POST.get('pswd')
        user = User.objects.create_superuser(username=uname,password=pswd)
        return redirect('reg')
    return render(request,'newadmin/register.html')