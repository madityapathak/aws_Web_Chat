from ast import Not
from friend.models import Friendlist
from django.db.models import Q
from django.shortcuts import render,redirect,HttpResponse
from friend.models import Friendlist

from notifications.models import Notification
from private_chat.models import ChatRoom
from .forms import UserForm,UpdateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from .models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from .utils import verification_token, password_reset_token,EmailThread
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import time
from datetime import datetime
import pytz

from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
import os
import cv2
import json
import base64
from django.core import files
TEMP_PROFILE_IMAGE_NAME = "temp_profile_image.png"


def send_activation_email(user, request):
    current_site=get_current_site(request)
    email_sub='Account activation'
    context={}
    context['user']=user
    context['domain']=current_site
    context['uid']=urlsafe_base64_encode(force_bytes(user.id))
    context['token']=verification_token.make_token(user)
    email_body=render_to_string('accounts/activation-email-string.html',context)
    email=EmailMessage(subject=email_sub,body=email_body,from_email=settings.EMAIL_HOST_USER, to=[user.email])
    EmailThread(email).start()


def password_reset_email(user, request):
    current_site=get_current_site(request)
    email_sub='Account Recovery'
    context={}
    context['user']=user
    context['domain']=current_site
    context['uid']=urlsafe_base64_encode(force_bytes(user.id))
    context['uname']=urlsafe_base64_encode(force_bytes(user.username))
    context['token']=password_reset_token.make_token(user)
    email_body=render_to_string('accounts/password-reset-string.html',context)
    email=EmailMessage(subject=email_sub,body=email_body,from_email=settings.EMAIL_HOST_USER, to=[user.email])
    EmailThread(email).start()


def activation_email_validator(request, uidb64, token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user=User.objects.get(id=uid)
    except Exception as e:
        user=None
   
    if user and user.is_verified==False and verification_token.check_token(user,token):
        try:
            new_friendlist=Friendlist.objects.get(user=user)
        except:
            new_friendlist=False
            
        if new_friendlist==False:
            Friendlist.objects.create(user=user)
        
        user.is_verified=True

        user.save()
        
        Notification.objects.create(
                from_user=user,
                for_user=user,
                body="welcome user"  )

        
        messages.error(request,'account verified you can log in now')
        return redirect('accounts:login')
      
    return render(request,'accounts/failed.html',{'user':user})

def password_email_validator(request, uidb64, token, unameb64):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user=User.objects.get(id=uid)
    except Exception as e:
        user=None
    
    
    if user and user.is_verified and password_reset_token.check_token(user,token):
        return redirect('accounts:reset-password',uidb64, unameb64)
    
    return render(request,'accounts/failed.html')




# Create your views here.
def log_in(request):
    
    if request.user.is_authenticated and request.user.is_verified:
        return redirect('accounts:home')
    
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        if email and password:
            try:
                user = User.objects.get(email=email)
            except:
                messages.error(request, 'enter correct email')

            user = authenticate(request, email=email, password=password)

            if user is not None:
                if user.is_verified:
                    login(request,user)
                    return redirect('accounts:home')
                else:
                    messages.error(request, 'your email is not verified')
                    # write code for verification hee
            else:
                messages.error(request, 'enter correct password')

        else:
            messages.error(request, 'Enter valid email and pasword')
       
    return render(request,'accounts/login.html')

def sign_up(request):
    context={}
    context['UserForm']=UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)

        pass1=request.POST.get("password1")
        pass2=request.POST.get("password2")
        usrn=request.POST.get("username")
        mail=request.POST.get("email")

        
        try:
            usr_1=User.objects.get(email=mail)
        except:
            usr_1=False
        if usr_1 and usr_1.is_verified==False:
            usr_1.delete()
            time.sleep(3)
        
        try:
            usr=User.objects.get(username=usrn)
        except:
            usr=False
        if usr and usr.is_verified==False:
            usr.delete()
            time.sleep(3)
                                                                                   
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            send_activation_email(user,request)
            messages.error(request,'an email has been sent to your email id kindly verify before login')
            return redirect('accounts:login')

        else:
            flag = False
            if usr_1:
                messages.error(request, "email is taken")
                flag = True
            if pass1 == pass2 and len(pass1) <= 7 :
                messages.error(request, 'password too short')
                flag = True
            if usr:
                messages.error(request, 'username is taken')
                flag = True
            if pass1 != pass2:
                messages.error(request, 'passwords did not match')
                flag = True
            if usrn.isnumeric():
                messages.error(request, 'username cannot be entirely numeric')
                flag = True
            if pass1 == pass2 and pass1.isnumeric():
                messages.error(request, 'password cannot be entirely numeric')
                flag = True
            if not flag:
                messages.error(request, 'Your password can’t be a commonly used password or too similar to your other personal information.')
            return redirect('accounts:signup')
            
    return render(request,"accounts/signup.html",context)


def account_search_page(request):
    context={}
    if request.method == 'POST':
        q = request.POST.get('email').lower()
        if q:
            user = User.objects.filter(
                Q(email__icontains=q) |
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q)
                ).exclude(is_verified='False')
            if user:
                context['users']=user
            else:
                context['non_e']=True
        else:
            messages.error(request, 'enter email') 
    return render(request,"accounts/password_reset_search.html",context)
    

    
def log_out(request):
    request.user.save()
    logout(request)
    return redirect ('accounts:login')

def send_password_reset_email(request,pk):
    context={}
    user=User.objects.get(username=pk)
    password_reset_email(user,request)
    messages.error(request,'password reset mail sent to linked email id')
    return redirect('accounts:login')

def update_password(request,uidb64,unameb64):
    
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        uname=force_str(urlsafe_base64_decode(unameb64))
        user1=User.objects.get(id=uid)
        user2=User.objects.get(username=uname)
        if user1==user2:
            user=user1
        else:
            user=False
    except:
        user=False
        
    
    if request.method=='POST':
        
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1==password2:
            user=User.objects.get(id=uid)
            user.set_password(password1)
            user.save()
            messages.error(request,'password reset successful kindly login with new password')
            return redirect('accounts:login')
        else:
            messages.error(request, 'password missmatch')
       
    return render(request,'accounts/update-password.html',{'user':user})


@login_required(login_url='accounts:login')
def home(request):
    request.user.save()
    context={}
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    if q!='':
        users = User.objects.filter(
            Q(email__icontains=q) |
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q)
            ).exclude(is_verified='False')
        if users:
            context['users']=users
    friend=Friendlist.objects.get(user=request.user)
    friends=friend.friends.all()
    notifications=Notification.objects.filter(for_user=request.user)
    context["notifications"]=notifications
    context['friends']=friends

    chats=ChatRoom.objects.filter( Q(participant1=request.user) | Q(participant2=request.user))
    context['chats']=chats


    dict={}
    for chat in chats:
        if chat.message_set.all().last():
            dict[chat.id]=[str(chat.message_set.all().last().body),chat.message_set.all().last().created.isoformat()]
        else:
            dict[chat.id]=["No messages currently.....","start chat ?..."]
    context['message_set']=json.dumps(dict)
    
     
    # print(json.dumps(dict),"----------------------------")







    return render(request, 'accounts/home.html',context)


@login_required(login_url='accounts:login')
def edit_account(request,pk):
    request.user.save()
    try:
        user=User.objects.get(id=pk)
    except:
        user=False
    context={}
    if user == request.user:
        context["user_update_form"]=UpdateUserForm(instance=user)
        has_profile_image="profile_images/"+pk+"/profile_image.png"
        if user.profile_image==has_profile_image:
            context['show_remove_image_button']= True
        context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
        context['user']=user
        if request.method=='POST':

            fname=request.POST.get("first_name")
            lname=request.POST.get("last_name")
            abt=request.POST.get("about")
            
            # image=request.FILES['profile_image']--> this is used to get images from POST method
            form = UpdateUserForm(request.POST,instance=user)
            if form.is_valid():
                form.save()
                Notification.objects.create(
                    from_user=user,
                    for_user=user,
                    body="about updated"    )
                return redirect('friend:profile',user.username)
            else:
                if not len(fname.strip()):
                    messages.error(request, 'First Name is required')
                if not len(lname.strip()):
                    messages.error(request, 'Last Name is required')
                if not len(abt.strip()):
                    messages.error(request, 'About is required')
                return redirect('accounts:edit-account',user.id)

        return render(request,'accounts/editaccount.html',context)
        

    else:
        return render(request,'friend/inaccessible.html',context)



def save_temp_profile_image_from_base64String(imageString, user):
	INCORRECT_PADDING_EXCEPTION = "Incorrect padding"
	try:
		if not os.path.exists(settings.TEMP):
			os.mkdir(settings.TEMP)
		if not os.path.exists(settings.TEMP + "/" + str(user.pk)):
			os.mkdir(settings.TEMP + "/" + str(user.pk))
		url = os.path.join(settings.TEMP + "/" + str(user.pk),TEMP_PROFILE_IMAGE_NAME)
		storage = FileSystemStorage(location=url)
		image = base64.b64decode(imageString)
		with storage.open('', 'wb+') as destination:
			destination.write(image)
			destination.close()
		return url
	except Exception as e:
		print("exception: " + str(e))
		# workaround for an issue I found
		if str(e) == INCORRECT_PADDING_EXCEPTION:
			imageString += "=" * ((4 - len(imageString) % 4) % 4)
			return save_temp_profile_image_from_base64String(imageString, user)
	return None



def crop_image(request, *args, **kwargs):
    payload = {}
    user = request.user
    has_profile_image="profile_images/"+str(request.user.id)+"/profile_image.png"
    if request.POST and user.is_authenticated:
        try:
            imageString = request.POST.get("image")
            url = save_temp_profile_image_from_base64String(imageString, user)
            img = cv2.imread(url)

            cropX = int(float(str(request.POST.get("cropX"))))
            cropY = int(float(str(request.POST.get("cropY"))))
            cropWidth = int(float(str(request.POST.get("cropWidth"))))
            cropHeight = int(float(str(request.POST.get("cropHeight"))))
            if cropX < 0:
                cropX = 0
            if cropY < 0: # There is a bug with cropperjs. y can be negative.
                cropY = 0
            crop_img = img[cropY:cropY+cropHeight, cropX:cropX+cropWidth]
            
            cv2.imwrite(url, crop_img)
            
            # delete the old image
            if user.profile_image==has_profile_image:
                user.profile_image.delete()
            
            # Save the cropped image to user model
            user.profile_image.save("profile_image.png", files.File(open(url, 'rb')))
            user.save()
            
            friend=Friendlist.objects.get(user=user)
            for people in friend.friends.all():
                Notification.objects.create(
                    from_user=user,
                    for_user=people,
                    body="friend profileimg change"  )
            Notification.objects.create(
                    from_user=user,
                    for_user=user,
                    body="profileimg change"  )

            
            payload['result'] = "success"
            payload['cropped_profile_image'] = user.profile_image.url
            
            # delete temp file
            os.remove(url)
        except Exception as e:
            print("exception: " + str(e))
            payload['result'] = "error"
            payload['exception'] = str(e)
    else:
        return render(request,'friend/inaccessible.html')
    return HttpResponse(json.dumps(payload), content_type="application/json")




def remove_profile_image(request):
    payload={}
    if request.method=="POST":
        id=request.POST.get("user_id")
        try:
            user=User.objects.get(id=id)
        except:
            user=False
        
        if user==request.user:
            has_profile_image="profile_images/"+str(request.user.id)+"/profile_image.png"
            if user.profile_image==has_profile_image:
                user.set_profile_image_to_default()
            else:
                payload["status"]="something went wrong"    
        else:
            return render(request,'friend/inaccessible.html') 
    else:
        return render(request,'friend/inaccessible.html')            
    return HttpResponse(json.dumps(payload), content_type="application/json")

def about_page(request):
    return render(request,'accounts/about.html')