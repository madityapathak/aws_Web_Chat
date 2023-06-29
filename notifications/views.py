from django.shortcuts import render,HttpResponse,redirect
from .models import Notification
import json
from datetime import datetime
import pytz
from Web_Chat.utils import remove_duplicates_from_table
from django.contrib.auth.decorators import login_required
# Create your views here.




@login_required(login_url='accounts:login')
def notification_page(request):
    request.user.save()
    context={}
    #remove_duplicates_from_table(Notification,['from_user','for_user','body','room_group','room_name'])
    notifications=Notification.objects.filter(for_user=request.user)

    count=Notification.objects.filter(for_user=request.user,is_seen=False).count()
    context['count'] = count
    context["notifications"] = notifications
    return render(request,'notifications/notificationpage.html',context)


@login_required(login_url='accounts:login')
def delete_notification(request):
    payload={}
    
    if request.method == "POST":
        id=request.POST.get("id")
        try:
            notification=Notification.objects.get(id=id)
        except:
            notification=False
        if notification and notification.for_user == request.user:
            notification.delete()
            payload["status"]="success"
            return HttpResponse(json.dumps(payload), content_type="application/json")
        else:
            payload['status']='something went wrong'
            return HttpResponse(json.dumps(payload), content_type="application/json")
    else:
        return render(request,'public_chat/inaccessible.html')

@login_required(login_url='accounts:login')
def delete_all_notifications(request):
    context={}
    if not request.user:
        context['inheritance_2']=True
    context['obj']='all notifications'
    if request.method=='POST':
        notifications=Notification.objects.filter(for_user=request.user)
        notifications.delete()
        return redirect ('notifications:notification')
    return render(request,'public_chat/delete.html',context)

@login_required(login_url='accounts:login')
def seen_status(request):
    request.user.save()
    payload={}
    if request.method == 'POST':
        id=request.POST.get('id')

        try:
            notification=Notification.objects.get(id=id)
        except:
            notification=False

        if notification:
            notification.is_seen=True
            notification.save()
            payload['status']='success'
            return HttpResponse(json.dumps(payload), content_type="application/json")

        else:
            payload['status']='somethin went wrong'
            return HttpResponse(json.dumps(payload), content_type="application/json")

            
    else:
        return render(request,'public_chat/inaccessible.html')
