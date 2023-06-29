from django.shortcuts import render,redirect,HttpResponse
from .models import ChatRoom,Message
import json
from notifications.models import Notification
from django.contrib.auth.decorators import login_required
from django.conf import settings
# Create your views here.

@login_required(login_url='accounts:login')
def chat(request,pk):
    context={}
    try:
        room=ChatRoom.objects.get(id=pk)
    except:
        room=False
    if room:
        context["debug_mode"]=settings.DEBUG
        if request.user == room.participant1 or request.user == room.participant2:

            if request.user == room.participant1:
                oth=room.participant2
            else:
                oth=room.participant1
            context['heading_user']=oth
            message_set=Message.objects.filter(room=room,user=oth,is_seen=False)
            for msg in message_set:
                msg.is_seen=True
                msg.save()

            message=Message.objects.filter(room=room,visible_to=request.user)
            context['messages']=message
            context['room_id']=pk    
            if room.freezer:
                context['freeze_status']='freezed'
                context["freezer"]=room.freezer.email
                context["me"]=request.user.email
            else:
                context['freeze_status']='unfreezed'    
            if request.method=='POST':
                if request.POST.get('body'):
                    text_val=request.POST.get('body')
                    if len(text_val.strip()):
                        msg=Message.objects.create(
                            body=request.POST.get('body'),
                            room=room,
                            user=request.user)
                        msg.visible_to.add(room.participant1,room.participant2)
                    return redirect('private_chat:chatroom',pk=room.id)
            return render(request,'private_chat/chatroom.html',context)
        else:
            return render(request,'private_chat/inaccessible.html')
    else:
        return render(request,'private_chat/inaccessible.html')

@login_required(login_url='accounts:login')
def delete_conversation(request):
    payload={}
    user=request.user
    if request.method=='POST':
        try:
            room_id=request.POST.get("room_id")
        except:
            room_id=False
        if room_id:
            try:
                room=ChatRoom.objects.get(id=room_id)
            except:
                room=False
            if room:
                if user==room.participant1 or user==room.participant2:
                    messages=room.message_set.all()
                    for message in messages:
                        message.visible_to.remove(request.user)
                    delmes=Message.objects.filter(visible_to=None)
                    delmes.delete()
                    payload["done"]='done'
        
    
    # else:
    #     return render(request,'friend/inaccessible.html')
    # return HttpResponse(json.dumps(payload), content_type="application/json")
    return render(request,'friend/inaccessible.html')

@login_required(login_url='accounts:login')
def freeze_chat(request):   
    payload={}
    user=request.user
    if request.method == 'POST':
        try:
            room_id=request.POST.get('room_id')
        except:
            room_id=False
        if room_id:
            try:
                room=ChatRoom.objects.get(id=room_id)
            except:
                room=False
            if room and not room.freezer:
                if user==room.participant1 or user==room.participant2:
                    room.freezer=request.user
                    room.save()

                    if request.user == room.participant1:
                        participant = room.participant2
                    else:
                        participant=room.participant1

                    Notification.objects.create(
                        from_user=request.user,
                        for_user=participant,
                        body="user freezed chat"  )

                    Notification.objects.create(
                        from_user=participant,
                        for_user=request.user,
                        body="you freezed chat"  )
                
        #         payload["done"]='done'
        #         return HttpResponse(json.dumps(payload), content_type="application/json")
        #     payload['status']='chatroom query does not exist'
        #     return HttpResponse(json.dumps(payload), content_type="application/json") 
        # payload['status']='invalid room id'
        # return HttpResponse(json.dumps(payload), content_type="application/json")       
    return render(request,'private_chat/inaccessible.html')


@login_required(login_url='accounts:login')   
def unfreeze_chat(request):
    payload={}
    user=request.user
    if request.method=='POST':
        try:
            room_id=request.POST.get('room_id')
        except:
            room_id=False
        if room_id:
            try:
                room=ChatRoom.objects.get(id=room_id)
            except:
                room=False
            if room and room.freezer:
                if user==room.participant1 or user==room.participant2:
                    frezzer=room.freezer
                    room.freezer=None
                    room.save()

                    if frezzer == room.participant1:
                        participant = room.participant2
                    else:
                        participant=room.participant1

                    Notification.objects.create(
                        from_user=participant,
                        for_user=frezzer,
                        body="you unfroze chat"  )

                    Notification.objects.create(
                        from_user=frezzer,
                        for_user=participant,
                        body="user unfroze chat"  )
                    
        #             payload["done"]='done'
        #             return HttpResponse(json.dumps(payload), content_type="application/json")
        #     payload["status"]='matching query does not exist'
        #     return HttpResponse(json.dumps(payload), content_type="application/json")
        # payload["status"]='invalid room id'
        # return HttpResponse(json.dumps(payload), content_type="application/json")    
    # payload['status']='invalid request'
    return render(request,'private_chat/inaccessible.html')


@login_required(login_url='accounts:login')
def edit_message(request):
    if request.method=='POST':
        id=request.POST.get('msg_id')
        body=request.POST.get('body')
        try:
            message=Message.objects.get(id=id)
        except:
            message=False
        if message and request.user==message.user:
            if message.body.strip()==body.strip():
                return redirect('private_chat:chatroom',message.room.id)
            else:
                if len(body.strip())==0:
                    x=message.room.id
                    message.delete()
                    return redirect('private_chat:chatroom',x)
                else:    
                    x=int(message.update_status)
                    message.body=body
                    message.update_status=x+1
                    message.save()
                    return redirect('private_chat:chatroom',message.room.id)
        
        return render(request,'private_chat/inaccessible.html')
    else:
        return render(request,'private_chat/inaccessible.html')

@login_required(login_url='accounts:login')
def delete_a_message(request,pk):
    context={}
    try:
        msg=Message.objects.get(id=pk)
    except:
        msg=False
        context['inheritance_1']=True
    if msg:
        if request.user==msg.user:
            context['obj']=msg
        else:
            context['inheritance_2']=True
    if request.method=='POST':
        room=msg.room
        msg.delete()
        return redirect('private_chat:chatroom',room.id )
    return render(request,'private_chat/delete.html',context)