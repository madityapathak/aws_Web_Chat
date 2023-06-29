import json
from django.db import models
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from public_chat.models import GroupChatRoom

# Create your models here.


class Notification(models.Model):
    from_user= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='from_user')
    for_user= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,  related_name='for_user')
    body=models.TextField(max_length=200)
    room_group=models.ForeignKey(GroupChatRoom,on_delete=models.CASCADE,null=True,blank=True)
    room_name = models.CharField(max_length=152,blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    is_seen=models.BooleanField(default=False,null=False)


    class Meta:
        ordering = ['-created']






    def type(self):
        if self.body == "request received":
            return 1
        elif self.body == "request sent":
            return 2
        elif self.body == "unfriended you":
            return 3
        elif self.body == "you unfriended":
            return 4
        elif self.body == "you accepted request":
            return 5
        elif self.body == "user accepted request":
            return 6
        elif self.body == "you declined request":
            return 7
        elif self.body == "user declined request":
            return 8
        elif self.body == "request cancled":
            return 9
        elif self.body == "cancled request":
            return 10
        elif self.body == "removed by admin":
            return 11
        elif self.body == "admin removed user":
            return 12
        elif self.body == "you removed user":
            return 13
        elif self.body == "restricted by admin":
            return 14
        elif self.body == "admin restricted user":
            return 15
        elif self.body == "you restricted user":
            return 16
        elif self.body == "unrestricted by admin":
            return 17
        elif self.body == "admin unrestricted user":
            return 18
        elif self.body == "you unrestricted user":
            return 19
        elif self.body == "user joined group":
            return 20
        elif self.body == "you joind":
            return 21
        elif self.body == "you created":
            return 22
        elif self.body == "user left group":
            return 23
        elif self.body == "you left group":
            return 24
        elif self.body == "group admin left":
            return 25
        elif self.body == "you left your room":
            return 26
        elif self.body == "room deleted":
            return 27
        elif self.body == "you deleted room":
            return 28
        elif self.body == "room updated":
            return 29
        elif self.body == "you updated room":
            return 30
        elif self.body == "admin changed roomimg":
            return 31
        elif self.body == "changed roomimg":
            return 32
        elif self.body == "admin removed roomimg":
            return 33
        elif self.body == "removed roomimg":
            return 34
        elif self.body == "user freezed chat":
            return 35
        elif self.body == "you freezed chat":
            return 36
        elif self.body == "you unfroze chat":
            return 37
        elif self.body == "user unfroze chat":
            return 38
        elif self.body == "profileimg change":
            return 39
        elif self.body == "friend profileimg change":
            return 40
        elif self.body == "welcome user":
            return 41
        elif self.body == "about updated":
            return 42





    def save(self, *args, **kwargs):
        if len(Notification.objects.filter(from_user=self.from_user,for_user=self.for_user,body=self.body,room_group=self.room_group,room_name=self.room_name))>=1:
            Notification.objects.filter(from_user=self.from_user,for_user=self.for_user,body=self.body,room_group=self.room_group,room_name=self.room_name).delete()
        if self.room_group:
            channel_layer=get_channel_layer()
            async_to_sync(channel_layer.group_send)(
            self.for_user.username,{
                'type':'websocket_receive',
                "body": self.body,
                "from_user": self.from_user.username,
                "for_user": self.for_user.username,
                "room_id" :self.room_group.id,
                "room_name" : self.room_group.name,
                "host_username" : self.room_group.host.username
                })

        elif self.room_name and not self.room_group :
            channel_layer=get_channel_layer()
            async_to_sync(channel_layer.group_send)(
            self.for_user.username,{
                'type':'websocket_receive',
                "body": self.body,
                "from_user": self.from_user.username,
                "for_user": self.for_user.username,
                "roomname" :self.room_name,
                })

                
        else:
            channel_layer=get_channel_layer()
            async_to_sync(channel_layer.group_send)(
            self.for_user.username,{
                'type':'websocket_receive',
                "body": self.body,
                "from_user": self.from_user.username,
                "for_user": self.for_user.username
                })

        super(Notification,self).save(*args,**kwargs)


