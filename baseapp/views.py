from datetime import datetime
from django.utils import timezone
from django.shortcuts import redirect, render
from baseapp.models import Table
from django.db.models.lookups import GreaterThan
from django.contrib import messages
from baseapp.form import user_info_Forms
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .tasks import *
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json
import pytz
def home(request):
    return render(request,'baseapp/newhome.html')


@login_required
def user_logout(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'LOGGED OUT SUCCESSFULLY. ')
    return redirect("/baseapp/logins")


def list(request):
    if request.user.is_authenticated:
        currentime = datetime.now(pytz.timezone('Asia/Kolkata'))
        currdate = currentime.strftime("%Y-%m-%dT%H:%M")
        datalist = Table.objects.filter(Datetime__lte=currdate)
        
        for data in datalist:
           
            pt = PeriodicTask.objects.get(name=data.pk)
            pt.delete()
        
        datalist.delete()
       
        print(datalist)
        datalist=Table.objects.all().filter(user=request.user )
        print(datalist)
        return render(request,'baseapp/list.html',{"data":datalist})
    messages.add_message(request, messages.ERROR, 'LOGIN REQUIRED! ')
    return HttpResponseRedirect(reverse('baseapp:logins'))


def add(request):
    if request.user.is_authenticated:
        md=Table()
        user = User.objects.get(username=request.user)
        # print(user.username,user.email)
        currentime = datetime.now(pytz.timezone('Asia/Kolkata'))
        date_time = currentime.strftime("%Y-%m-%dT%H:%M")
        print(date_time)
        if request.method =='POST' :
            md.user=request.user
            md.title=request.POST["title"]
            md.desc=request.POST["Description"]
            md.Datetime = request.POST["DateTime"]
           
            # send_mail_task.apply_async(kwargs)
            if len(md.title) != 0 and len(md.desc) != 0 and md.Datetime>date_time :
                md.save()
                print(md.title)
                print(md.desc)
                print(md.Datetime)

                format ="%Y-%m-%dT%H:%M"
                
                Date = datetime.strptime(
                    md.Datetime, format)
                kwargs = (
                          user.username,
                          user.email,
                          md.title,
                          md.desc)
                schedule, created = CrontabSchedule.objects.get_or_create(
                hour=Date.hour, minute=Date.minute,month_of_year=Date.month,day_of_month=Date.day)
                task = PeriodicTask.objects.create(crontab=schedule,name=md.pk, task='baseapp.tasks.send_mail_task', args=json.dumps(kwargs))

                return redirect("/baseapp/list")
            else:
                messages.add_message(request, messages.ERROR, 'ENTER VALID DATA! ')
                return render(request,'baseapp/add.html')
        return render(request,'baseapp/add.html')
    messages.add_message(request, messages.ERROR, 'LOGIN REQUIRED! ')
    return HttpResponseRedirect(reverse('baseapp:logins'))
    

def deleteTask(request,pk):
    md = Table.objects.get(id=pk)
    pt = PeriodicTask.objects.get(name=md.pk)
    pt.delete()
    md.delete()
    return redirect('/baseapp/list')

def logins(request):
    if request.method == 'POST' and request.POST.get('case')== 'False':
        user_form=user_info_Forms(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            # sending mail to new register
            
            send_mail(
                'welcome mail to new user',
                'Hi '+ user.username+ "! you have registered successfully in our worlist wesbite",
                '',
                [user.email],
                fail_silently=False,
            )

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
