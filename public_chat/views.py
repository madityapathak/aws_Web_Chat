from pyexpat.errors import messages
from django.shortcuts import render,redirect,HttpResponse
from notifications.models import Notification
from public_chat.forms import GroupChatRoomForm
from.models import GroupChatRoom,GroupMessage
from django.contrib import messages
import json
from accounts.models import User
from django.db.models import Q
from datetime import datetime
import pytz
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
import os
import cv2
import json
import base64
from django.core import files
from django.contrib.auth.decorators import login_required
TEMP_ROOM_IMAGE_NAME = "temp_room_image.png"

@login_required(login_url='accounts:login')
def group_chat(request,pk):
    context={}
    
    try:
        room=GroupChatRoom.objects.get(id=pk)
    except:
        room=False
    if room:
        context["debug_mode"]=settings.DEBUG
        context['restricted_users']=room.restricted_to.all()
        context["room"]=room
        context['participants']=room.participants.all()
        messages=GroupMessage.objects.filter(room=room).exclude(invisible_to=request.user)
        context['messages']=messages
        if request.method=="POST":
            body=request.POST.get('body')
            if len(body.strip()):
                if request.user not in room.participants.all():
                    room.participants.add(request.user)
                    
                    for participant in room.participants.all():
                        if participant != request.user:
                            Notification.objects.create(
                                from_user=request.user,
                                for_user=participant,
                                room_group=room,
                                body="user joined group"    )
                    
                    Notification.objects.create(
                        from_user=room.host,
                        for_user=request.user,
                        room_group=room,
                        body="you joind"    )

                
                msg=GroupMessage.objects.create(
                    body=body,
                    room=room,
                    user=request.user)
            return redirect('public_chat:chatroom',pk=room.id)
        return render(request,'public_chat/group_chat.html',context)
    else:
        return render(request,'public_chat/inaccessible.html')

@login_required(login_url='accounts:login')
def create_room(request):

    request.user.save()

    context={}
    if request.method=="POST":
        name=request.POST.get("room_name").strip()
        des=request.POST.get("description").strip()
        topic=request.POST.get("room_topic").strip()
        chatroom=GroupChatRoom.objects.create(
                host=request.user,
                topic=topic,
                name=name,
                description=des)
        chatroom.save()
        Notification.objects.create(
            from_user=request.user,
            for_user=request.user,
            room_group=chatroom,
            body="you created"    )


        chatroom.participants.add(request.user)
        return redirect('public_chat:chatroom',chatroom.id)
    return render(request,'public_chat/createroom.html',context)

@login_required(login_url='accounts:login')
def home(request):
    context={}
    user_rooms=GroupChatRoom.objects.filter(participants=request.user)
    context['user_rooms']=user_rooms
    q = request.GET.get('q') if request.GET.get('q') != None else ''


    
    if q:
        public_rooms = GroupChatRoom.objects.filter(
            Q(name__icontains=q) |
            Q(topic__icontains=q)
            )
        context['total_rooms']=public_rooms.count()
        context['show_search_results']=True
    else:
        public_rooms = GroupChatRoom.objects.all()
        context['show_search_results']=False

    context["public_rooms"]=public_rooms

    
    return render(request,'public_chat/home.html',context)


@login_required(login_url='accounts:login')
def delete_a_message(request,pk):
    context={}
    try:
        msg=GroupMessage.objects.get(id=pk)
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
        return redirect('public_chat:chatroom',room.id )
    return render(request,'public_chat/delete.html',context)


@login_required(login_url='accounts:login')
def edit_message(request):
    if request.method=='POST':
        id=request.POST.get('msg_id')
        body=request.POST.get('body')
        try:
            message=GroupMessage.objects.get(id=id)
        except:
            message=False
        if message:
            if message.body.strip()==body.strip():
                return redirect('public_chat:chatroom',message.room.id)
            else:
                if len(body.strip())==0:
                    x=message.room.id
                    message.delete()
                    return redirect('public_chat:chatroom',x)
                else:    
                    x=int(message.update_status)
                    message.body=body
                    message.update_status=x+1
                    message.save()
                    return redirect('public_chat:chatroom',message.room.id)
        
        return render(request,'public_chat/inaccessible.html')
    else:
        return render(request,'public_chat/inaccessible.html')


@login_required(login_url='accounts:login')
def leave_room(request):
    payload={}
    if request.method=='POST':
        room_id=request.POST.get('room_id')
        try:
            room=GroupChatRoom.objects.get(id=room_id)
        except:
            room=False
        if room:
           
            
            if request.user in room.participants.all():
                room.participants.remove(request.user)


                if request.user==room.host:
                    for participant in room.participants.all():
                        Notification.objects.create(
                            from_user=request.user,
                            for_user=participant,
                            room_group=room,
                            body="group admin left"    )

                    Notification.objects.create(
                        from_user=room.host,
                        for_user=request.user,
                        room_group=room,
                        body="you left your room"    )

                    
                else:
                    for participant in room.participants.all():
                        Notification.objects.create(
                            from_user=request.user,
                            for_user=participant,
                            room_group=room,
                            body="user left group"    )

                    Notification.objects.create(
                        from_user=room.host,
                        for_user=request.user,
                        room_group=room,
                        body="you left group"    )

                
    #             return HttpResponse(json.dumps(payload), content_type="application/json")
    #     else:
    #         return render(request,'public_chat/inaccessible.html')
    # else:
    #     return render(request,'public_chat/inaccessible.html')
    return render(request,'public_chat/inaccessible.html')

@login_required(login_url='accounts:login')
def clear_convo(request):
    payload={}
    if request.method=='POST':
        room_id=request.POST.get('room_id')
        try:
            room=GroupChatRoom.objects.get(id=room_id)
            messages=GroupMessage.objects.filter(room=room)
        except:
            room=False
            message=False
        if room and messages:
            if request.user in room.participants.all():
                for message in messages:
                    message.invisible_to.add(request.user)
    #         return HttpResponse(json.dumps(payload), content_type="application/json")
    #     else:
    #         return render(request,'public_chat/inaccessible.html')
    # else:
    #     return render(request,'public_chat/inaccessible.html')
    return render(request,'public_chat/inaccessible.html')


@login_required(login_url='accounts:login')
def remove_user_from_group(request):
    payload={}
    if request.method=='POST':
        removiee_id=request.POST.get('removiee_id')
        room_id=request.POST.get('room_id')
        try:
            room=GroupChatRoom.objects.get(id=room_id)
            removiee=User.objects.get(id=removiee_id)
        except:
            room=False
            removiee=False
        if request.user==room.host and removiee in room.participants.all():
            room.participants.remove(removiee)
            Notification.objects.create(
                from_user=room.host,
                for_user=removiee,
                room_group=room,
                body="removed by admin"
            )

            Notification.objects.create(
                from_user=removiee,
                for_user=room.host,
                room_group=room,
                body="you removed user"
            )


            for participant in room.participants.all():
                if participant != room.host:
                    Notification.objects.create(
                    from_user=removiee,
                    for_user=participant,
                    room_group=room,
                    body="admin removed user"
                )

            
    #         return HttpResponse(json.dumps(payload), content_type="application/json")
    #     else:
    #         return render(request,'public_chat/inaccessible.html')
    # else:
    #     return render(request,'public_chat/inaccessible.html')
    return render(request,'public_chat/inaccessible.html')


@login_required(login_url='accounts:login')
def restrict_message(request):
    payload={}
    if request.method=="POST":
        room_id=request.POST.get('room_id')
        user_id=request.POST.get('restricted_id')
        try:
            room=GroupChatRoom.objects.get(id=room_id)
            user=User.objects.get(id=user_id)
        except:
            room=False
            user=False
        if request.user==room.host and user in room.participants.all():
            room.restricted_to.add(user)

            Notification.objects.create(
                from_user=room.host,
                for_user=user,
                room_group=room,
                body="restricted by admin"
            )

            Notification.objects.create(
                from_user=user,
                for_user=room.host,
                room_group=room,
                body="you restricted user"
            )


            for participant in room.participants.all():
                if participant != room.host and participant != user:
                    Notification.objects.create(
                    from_user=user,
                    for_user=participant,
                    room_group=room,
                    body="admin restricted user"    )

            
    #         return HttpResponse(json.dumps(payload), content_type="application/json")
    #     else:
    #         return render(request,'public_chat/inaccessible.html')
    # else:
    #     return render(request,'public_chat/inaccessible.html')
    return render(request,'public_chat/inaccessible.html')

@login_required(login_url='accounts:login')
def unrestrict_message(request):
    payload={}
    if request.method=="POST":
        room_id=request.POST.get('room_id')
        user_id=request.POST.get('unrestricted_id')
        try:
            room=GroupChatRoom.objects.get(id=room_id)
            user=User.objects.get(id=user_id)
        except:
            room=False
            user=False
        if request.user==room.host and user in room.restricted_to.all():
            room.restricted_to.remove(user)

            Notification.objects.create(
                from_user=room.host,
                for_user=user,
                room_group=room,
                body="unrestricted by admin"
            )

            Notification.objects.create(
                from_user=user,
                for_user=room.host,
                room_group=room,
                body="you unrestricted user"
            )


            for participant in room.participants.all():
                if participant != room.host and participant != user:
                    Notification.objects.create(
                    from_user=user,
                    for_user=participant,
                    room_group=room,
                    body="admin unrestricted user"  )


            
    #         return HttpResponse(json.dumps(payload), content_type="application/json")
    #     else:
    #         return render(request,'public_chat/inaccessible.html')
    # else:
    #     return render(request,'public_chat/inaccessible.html')
    return render(request,'public_chat/inaccessible.html')


@login_required(login_url='accounts:login')
def delete_room(request,pk):
    
    context={}
    try:
        room=GroupChatRoom.objects.get(id=pk)
    except:
        room=False
        context['inheritance_1']=True
    if room:
        if request.user==room.host:
            context['obj']=room.name
        else:
            context['inheritance_2']=True
    if room and request.method=='POST':


        for participant in room.participants.all():
            if participant != room.host:
                Notification.objects.create(
                    from_user=room.host,
                    for_user=participant,
                    room_name=room.name,
                    body="room deleted"  )

            else:
                Notification.objects.create(
                        from_user=request.user,
                        for_user=room.host,
                        room_name=room.name,
                        body="you deleted room"  )

        room.delete()
        return redirect('accounts:home')
    return render(request,'public_chat/delete.html',context)


@login_required(login_url='accounts:login')
def update_room(request,pk):
    request.user.save()
    try:
        room=GroupChatRoom.objects.get(id=pk)
    except:
        room=False
    context={}
    context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    
    
    if room:
        context["room"]=room
        context["room_update_form"]=GroupChatRoomForm(instance=room)
        has_room_image="room_images/"+pk+"/room_image.png"
        if room.room_image==has_room_image:
            context['show_remove_image_button']= True
        if room.host == request.user:
            
            
            if request.method=='POST':
                n_ame=request.POST.get("name")
                t_opic=request.POST.get("topic")
                d_es=request.POST.get("description")
                
                form = GroupChatRoomForm(request.POST,instance=room)
                if form.is_valid():
                    form.save()

                    for participant in room.participants.all():
                        if participant != room.host:
                            Notification.objects.create(
                                from_user=room.host,
                                for_user=participant,
                                room_group=room,
                                body="room updated"  )
                        else:
                            Notification.objects.create(
                                from_user=request.user,
                                for_user=room.host,
                                room_group=room,
                                body="you updated room"  )


                    
                    return redirect('public_chat:chatroom',room.id)
                else:
                    if not len(n_ame.strip()):
                        messages.error(request, 'room name is required')
                    if not len(t_opic.strip()):
                        messages.error(request, 'a topic for room is required')
                    if not len(d_es.strip()):
                        messages.error(request, 'a short description of room is required')
                    return redirect('public_chat:update-room',room.id)
    else:
        return render(request,"public_chat/inaccessible.html")
    return render(request,"public_chat/editroom.html",context)





def save_temp_room_image_from_base64String(imageString, room):
	INCORRECT_PADDING_EXCEPTION = "Incorrect padding"
	try:
		if not os.path.exists(settings.ROOM_TEMP):
			os.mkdir(settings.ROOM_TEMP)
		if not os.path.exists(settings.ROOM_TEMP + "/" + str(room.pk)):
			os.mkdir(settings.ROOM_TEMP + "/" + str(room.pk))
		url = os.path.join(settings.ROOM_TEMP + "/" + str(room.pk),TEMP_ROOM_IMAGE_NAME)
		storage = FileSystemStorage(location=url)
		image = base64.b64decode(imageString)
		with storage.open('', 'wb+') as destination:
			destination.write(image)
			destination.close()
		return url
	except Exception as e:
		print("exception: " + str(e))
		if str(e) == INCORRECT_PADDING_EXCEPTION:
			imageString += "=" * ((4 - len(imageString) % 4) % 4)
			return save_temp_room_image_from_base64String(imageString, room)
	return None



def crop_image(request, *args, **kwargs):
    payload = {}
    user=request.user
    if request.POST and user.is_authenticated:
        try:

            id=request.POST.get("id")
            room=GroupChatRoom.objects.get(id=id)
            

            imageString = request.POST.get("image")
            url = save_temp_room_image_from_base64String(imageString, room)
            img = cv2.imread(url)

            cropX = int(float(str(request.POST.get("cropX"))))
            cropY = int(float(str(request.POST.get("cropY"))))
            cropWidth = int(float(str(request.POST.get("cropWidth"))))
            cropHeight = int(float(str(request.POST.get("cropHeight"))))
            if cropX < 0:
                cropX = 0
            if cropY < 0: # There is a bug with cropperjs. y can be negative.
                cropY = 0

            has_room_image="room_images/"+ str(room.id) +"/room_image.png"
            crop_img = img[cropY:cropY+cropHeight, cropX:cropX+cropWidth]
            
            cv2.imwrite(url, crop_img)
            if room.room_image==has_room_image:
                room.room_image.delete()
            room.room_image.save("room_image.png", files.File(open(url, 'rb')))
            room.save()

            for participant in room.participants.all():
                if participant != room.host :
                    Notification.objects.create(
                        from_user=room.host,
                        for_user=participant,
                        room_group=room,
                        body="admin changed roomimg"  )
                else:
                    Notification.objects.create(
                        from_user=request.user,
                        for_user=room.host,
                        room_group=room,
                        body="changed roomimg"  )

            payload['result'] = "success"
            payload['cropped_room_image'] = room.room_image.url
            os.remove(url)
        except Exception as e:
            print("exception: " + str(e))
            payload['result'] = "error"
            payload['exception'] = str(e)
    else:
        return render(request,'public_chat/inaccessible.html')
    return HttpResponse(json.dumps(payload), content_type="application/json")

@login_required(login_url='accounts:login')
def remove_room_image(request):
    payload={}
    if request.method=="POST":
        id=request.POST.get("id")
        try:
            room=GroupChatRoom.objects.get(id=id)
        except:
            room=False
        
        if request.user in room.participants.all():
            has_room_image="room_images/"+ str(room.id) +"/room_image.png"
            if room.room_image==has_room_image:
                room.set_room_image_to_default()

                for participant in room.participants.all():
                    if participant != room.host :
                        Notification.objects.create(
                            from_user=room.host,
                            for_user=participant,
                            room_group=room,
                            body="admin removed roomimg"  )
                    else:
                        Notification.objects.create(
                            from_user=request.user,
                            for_user=room.host,
                            room_group=room,
                            body="removed roomimg"  )                
    #         else:
    #             payload["status"]="something went wrong"    
    #     else:
    #         return render(request,'public_chat/inaccessible.html') 
    # else:
    #     return render(request,'public_chat/inaccessible.html')            
    # return HttpResponse(json.dumps(payload), content_type="application/json")
    return render(request,'public_chat/inaccessible.html')