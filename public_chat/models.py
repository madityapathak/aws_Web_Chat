from django.db import models
from django.conf import settings
# Create your models here.



def get_room_image_filepath(self, filename):
	return 'room_images/' + str(self.pk) + '/room_image.png'

def get_default_room_image():
	return "webchat/default_room_image.png"







class GroupChatRoom(models.Model):
    room_image=models.ImageField(max_length=255, upload_to=get_room_image_filepath, null=True, blank=True, default=get_default_room_image)
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    topic = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=250)
    participants=models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='participant_set')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    restricted_to=models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='restriction_set')

    def set_room_image_to_default(self):
            self.room_image.delete()
            self.room_image = get_default_room_image()
            self.save()





# we are getting descriptiion null error on migrate because some where in code while creation object of 
#  groupchatroom we have left the description field


# look for such bugs in all models creating calls like in notification model room_name field can raise issues in migration






class GroupMessage(models.Model):
    body=models.TextField()
    room=models.ForeignKey(GroupChatRoom,on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='group_message_user')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    update_status=models.CharField(max_length=3,default=0)
    invisible_to=models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='visible_groupmessage_set')
# we used invisible to field here instead of visible to because the use of visible to field
# will create a bug due to which new user will not be able to see previous messages of group
# because he was not the member of the group at the old messages were created
# we can use a logic to add new user to visible to fiels of all messages but this will result
# in making our database bulky and slow 

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.body[0:50]