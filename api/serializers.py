from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


from public_chat.models import GroupChatRoom
from accounts.models import User


class RoomsSerilizer(ModelSerializer):
    class Meta:
        model = GroupChatRoom
        fields = ['id','topic','name','description','updated','created','host','participants']

class UsersSerilizer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','email','username','about','last_active']