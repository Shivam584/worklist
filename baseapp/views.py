from django.utils import timezone
from django.shortcuts import redirect, render
from baseapp.models import Table
from django.contrib import messages
from baseapp.form import user_info_Forms
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request,'baseapp/newhome.html')


@login_required
def user_logout(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'LOGGED OUT SUCCESSFULLY. ')
    return redirect("/baseapp/logins")


def list(request):
    if request.user.is_authenticated:
        datalist=Table.objects.all().filter(user=request.user)
        print(datalist)
        return render(request,'baseapp/list.html',{"data":datalist})
    messages.add_message(request, messages.ERROR, 'LOGIN REQUIRED! ')
    return HttpResponseRedirect(reverse('baseapp:logins'))


def add(request):
    if request.user.is_authenticated:
        context={
            'error':False
                }  
        md=Table()
        if request.method =='POST' :
            md.user=request.user
            md.title=request.POST["title"]
            md.desc=request.POST["Description"]
            md.Datetime = timezone.now()
            if len(md.title) != 0 and len(md.desc) != 0:
                md.save()
                print(md.title)
                print(md.desc)
                print(md.Datetime)
                return redirect("/baseapp/list")
            else:
                context['error']=True;
                return render(request,'baseapp/add.html',context)
        else:
            print("not found")
        return render(request,'baseapp/add.html',context)
    messages.add_message(request, messages.ERROR, 'LOGIN REQUIRED! ')
    return HttpResponseRedirect(reverse('baseapp:logins'))
    

def deleteTask(request,pk):
    md = Table.objects.get(id=pk)
    md.delete()
    return redirect('/baseapp/list')

def logins(request):
    if request.method == 'POST' and request.POST.get('case')== 'False':
        user_form=user_info_Forms(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            messages.add_message(request, messages.SUCCESS, 'REGISTERED SUCCESSFULLY ')
        else:
            messages.add_message(request, messages.ERROR, 'ENTER VALID DETAILS OR USERNAME ALREADY EXIST ! ')
            
    elif request.method == 'POST' and request.POST.get('case') == 'True':
        
         username = request.POST.get('username')
         password=request.POST.get('password')
         print(username,password)
         user =authenticate(username=username,password=password)
         if user:
            if user.is_active:
                login(request,user)
                messages.add_message(request, messages.SUCCESS, 'LOGGED IN SUCCESSFULLY! ')
                return redirect("/baseapp/add")
            else:
                messages.add_message(request, messages.ERROR, 'ACCOUNT IS NOT ACTIVE! ')
         else:
            messages.add_message(request, messages.ERROR, 'ACCOUNT IS NOT PRESENT! ')
    return render(request, 'baseapp/logins.html')
