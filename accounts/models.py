from django.db import models
from django.contrib.auth.models import AbstractUser




def get_profile_image_filepath(self, filename):
	return 'profile_images/' + str(self.pk) + '/profile_image.png'

def get_default_profile_image():
	return "webchat/default_profile_image.png"





class User(AbstractUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email=models.EmailField(unique=True)
    profile_image=models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)
    hide_email=models.BooleanField(default=True)
    is_verified=models.BooleanField(default=False,null=False)
    updated = models.DateTimeField(auto_now=True)
    about=models.TextField()
    last_active=models.DateTimeField(auto_now=True,null=True,blank=True)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def set_profile_image_to_default(self):
        self.profile_image.delete()
        self.profile_image = get_default_profile_image()
        self.save()