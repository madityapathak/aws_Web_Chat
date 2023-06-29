from django.db import models
from django.conf import settings
# Create your models here.
class ChatRoom(models.Model):
    participant1=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='participant1')
    participant2=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='participant2')
    freezer=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.CASCADE,related_name='freezer')


class Message(models.Model):
    body=models.TextField()
    room=models.ForeignKey(ChatRoom,on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    update_status=models.CharField(max_length=3,default=0)
    created = models.DateTimeField(auto_now_add=True)
    visible_to=models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='visible_message_set')
    is_seen=models.BooleanField(default=False,null=False)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.body[0:50]