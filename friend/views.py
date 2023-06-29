from time import time, timezone
from django.contrib import messages
from accounts.models import User
from django.shortcuts import render,HttpResponse
from .models import Friendlist,Friend_request
from .utils import get_friend_req_or_false
import json
from private_chat.utils import create_or_get_chatroom,chatroom_or_false
from notifications.models import Notification
from public_chat.models import GroupChatRoom
from datetime import datetime
import pytz
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='accounts:login')
def profile(request,pk):
    if request.user.is_authenticated:
        
        request.user.save()
        me=request.user
        try:
            user=User.objects.get(username=pk)
        except:
            user=False
        context={}
        
        if user and user.is_verified:
            
            context['user']=user
            friend=Friendlist.objects.get(user=user)
            friends=friend.friends.all()
            context['friend_count']=friends.count()
            context['room_count']=GroupChatRoom.objects.filter(participants=user).count()
            # on successful signup create a friendlist in database automatically using the email verificatin function its important
            if chatroom_or_false(request,user.id):
                context['chatroom']=chatroom_or_false(request,user.id)
                context["msg_button"]='visible'
            else:
                context["msg_button"]='invisible'
                
            if me==user:
                context["status"]="self_profile"
            
                #edit profile button here
            else:
                context["id"]=pk
                if user in friends:
                    context["status"]="is_friend"
                    
                    #message button inthis case
                else:
                    #means they are not friends
                    if get_friend_req_or_false(sender=me, reciever=user):
                    #friend request sent
                    #cancle request button
                        context["status"]="friend_req_sent"
                    elif get_friend_req_or_false(sender=user, reciever=me):
                        context["status"]="pending_friend_req"
                        context["friend_req_id"]=get_friend_req_or_false(sender=user, reciever=me).id
                        
                        #accept and decline button here
                    else:
                        context["status"]="send_friend_req"
                        #send friend request button here
        else:
            return render(request,'friend/inaccessible.html')
    else:
        return HttpResponse("you are not authenticated")
    
    
    return render(request,"friend/profile.html",context)





@login_required(login_url='accounts:login')
def unfriend(request):
    payload={}
    remover=request.user
    if request.method=="POST":
        id=request.POST.get("user_id")
        try:
            removiee=User.objects.get(username=id)
        except Exception as e:
            removiee = False
            
        if removiee: 
            remover_friend_list=Friendlist.objects.get(user=remover)
            removiee_friend_list=Friendlist.objects.get(user=removiee)
            
            if remover in removiee_friend_list.friends.all():
                removiee_friend_list.friends.remove(remover)
            if removiee in remover_friend_list.friends.all():    
                remover_friend_list.friends.remove(removiee)
            payload["unfriended"]="unfriended"
            Notification.objects.create(
                        from_user=request.user,
                        for_user=removiee,
                        body="unfriended you" )
            Notification.objects.create(
                        from_user=removiee,
                        for_user=request.user,
                        body="you unfriended" )

            
        else:
            payload['response'] = f"Something went wrong: {str(e)}"

    else:
        return render(request,'friend/inaccessible.html')       

    return HttpResponse(json.dumps(payload), content_type="application/json")

@login_required(login_url='accounts:login')
def cancle_request(request):
    payload={}
    sender=request.user
    if request.method=="POST":
        id=request.POST.get("user_id")
        try:
            reciever=User.objects.get(username=id)
        except:
            reciever=False
        if reciever:
            try:
                requests=Friend_request.objects.filter(sender=sender,reciever=reciever,is_active=True)
            except:
                requests=False    
            if requests:
                if len(requests)>1:
                    for request in requests:
                        request.is_active=False
                        request.save()
                    payload["response"]="friend req cancled"
                    Notification.objects.create(
                        from_user=reciever,
                        for_user=sender,
                        body= "request cancled" ) 
                    Notification.objects.create(
                        from_user=sender,
                        for_user=reciever,
                        body= "cancled request" )  



                        
                else:
                    request=requests.first()
                    request.is_active=False
                    request.save()
                    payload["response"]="friend req cancled"
                    Notification.objects.create(
                        from_user=reciever,
                        for_user=sender,
                        body= "request cancled" )
                    Notification.objects.create(
                        from_user=sender,
                        for_user=reciever,
                        body= "cancled request" ) 




            else:
                messages.error(request,"recently acted on your friend request")
                payload["response"]="something went wrong"
       
    else:
        return render(request,'friend/inaccessible.html')       
        
    return HttpResponse(json.dumps(payload), content_type="application/json")


@login_required(login_url='accounts:login')
def send_request(request):
    payload={}
    sender=request.user
    if request.method=="POST":
        id=request.POST.get("user_id")
        try:
            reciever=User.objects.get(username=id)
            if reciever and reciever.is_verified:
                try:
                    reverse_req=Friend_request.objects.filter(sender=reciever,reciever=sender,is_active=True)
                    requests=Friend_request.objects.filter(sender=sender,reciever=reciever,is_active=False)
                    if reverse_req:
                        messages.error(request,"recently sent you friend request")
                    elif requests:
                        Notification.objects.create(
                            from_user=request.user,
                            for_user=reciever,
                            body= "request received" )
                        Notification.objects.create(
                            from_user=reciever,
                            for_user=request.user,
                            body="request sent" )
                        
                        if len(requests)>1:
                            for request in requests:
                                request.is_active=True
                                request.save()
                            payload["response"]="friend req sent"
                        else:
                            request=requests.first()
                            request.is_active=True
                            request.save()
                            payload["response"]="friend req sent"
                    else:
                        Friend_request.objects.create(
                            sender=sender,
                            reciever=reciever   )
                        Notification.objects.create(
                            from_user=request.user,
                            for_user=reciever,
                            body= "request received" ) 
                        Notification.objects.create(
                            from_user=reciever,
                            for_user=request.user,
                            body= "request sent" )



                        
                        payload["response"]="friend req sent"
                except:
                    payload["response"]="something went wrong"


        except Exception as e:
            payload['response'] = f"Something went wrong: {str(e)}"
       
    else:
        return render(request,'friend/inaccessible.html')       
        
    return HttpResponse(json.dumps(payload), content_type="application/json")

@login_required(login_url='accounts:login')
def accept(request):
    payload={}
    if request.method=="POST":
        id=request.POST.get("user_id")
        
        try:
            req=Friend_request.objects.get(id=id)
            
            if req.reciever==request.user and req.is_active:
                user=Friendlist.objects.get(user=request.user)
                user.friends.add(req.sender)
                oth_user=Friendlist.objects.get(user=req.sender)
                oth_user.friends.add(req.reciever)
                req.is_active=False
                #create chatroom
                chatroom_id=create_or_get_chatroom(request,req.sender.id)
                
                Notification.objects.create(
                        from_user=req.sender,
                        for_user=request.user,
                        body="you accepted request" )
                Notification.objects.create(
                        from_user=request.user,
                        for_user=req.sender,
                        body="user accepted request" )
               



                req.save()
            else:
                messages.error(request,"has cancled the request")
                return HttpResponse("something went wrong try resending the request")
                


        except:
            payload['response']="something went wrong"
            return HttpResponse("something went wrong")

    else:
        return render(request,'friend/inaccessible.html')
    return HttpResponse(json.dumps(payload), content_type="application/json")
    
@login_required(login_url='accounts:login')
def decline(request):
    payload={}
    if request.method=="POST":
        id=request.POST.get("user_id")
        try:
            req=Friend_request.objects.get(id=id)
            if req.sender == request.user:
                oth_usr=req.reciever
            elif req.reciever == request.user:
                oth_usr=req.sender
            
            if req.is_active:
                req.is_active=False
                req.save()

                Notification.objects.create(
                        from_user=oth_usr,
                        for_user=request.user,
                        body="you declined request" )
                Notification.objects.create(
                        from_user=request.user,
                        for_user=oth_usr,
                        body="user declined request" )

            else:
                messages.error(request,"recently cancled the friend request")

                
        except:
            return HttpResponse("something went wrong")

    else:
        return render(request,'friend/inaccessible.html')
    return HttpResponse(json.dumps(payload), content_type="application/json")

@login_required(login_url='accounts:login')
def friend_list(request,pk):
    request.user.save()
    context={}
    try:
        user=User.objects.get(id=pk)
    except:
        user=False
    if user:
        context['user']=user
        friend_s=Friendlist.objects.get(user=user)
        friendslist=friend_s.friends.all()
        context['friends']=friendslist
    else:
        return render(request,'friend/inaccessible.html') 
    return render(request,'friend/friendlist.html',context)


@login_required(login_url='accounts:login')
def sent_requests_view(request):
    request.user.save()
    context={}
    try:
        requests=Friend_request.objects.filter(sender=request.user,is_active=True)
    except:
        requests=False
    context['requests']=requests
    return render(request,'friend/sent_request.html',context)

@login_required(login_url='accounts:login')
def recieved_requests_view(request):
    request.user.save()
    context={}
    try:
        requests=Friend_request.objects.filter(reciever=request.user,is_active=True)
    except:
        requests=False
    context['requests']=requests
    return render(request,'friend/recieved_request.html',context)

@login_required(login_url='accounts:login')
def email_status_view(request):
    payload={}
    if request.method=="POST":
        username=request.POST.get("username")
        try:
            user=User.objects.get(username=username)
            if user == request.user:
                if user.hide_email:
                    user.hide_email=False
                    user.save()
                else:
                    user.hide_email=True
                    user.save()
            else:
                messages.error(request,"something went wrong")
        except:
            return HttpResponse("something went wrong")
    else:
        return render(request,'friend/inaccessible.html')
    return HttpResponse(json.dumps(payload), content_type="application/json")