from django.db import models

# Create your models here.
from django.conf import settings
from django.utils import timezone


class FriendRequestManager(models.Manager):
    def create_friend_request(self, sender, receiver):
        if self.filter(sender=sender, receiver=receiver).exists():
            return None
        return self.create(sender=sender, receiver=receiver)

class Friend_request(models.Model):
    sender=models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE, related_name="sender")
    reciever=models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE, related_name="reciever")
    is_active= models.BooleanField(blank=False, null=False, default=True)
    send_time =models.DateTimeField(auto_now_add=True)

    objects = FriendRequestManager()

    def __str__(self):

        return f"{self.id} - {self.sender} to {self.reciever}"
    




class Friendlist(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="user")
    friends=models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True, related_name="friends")
    