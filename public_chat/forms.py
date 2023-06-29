from django.forms import ModelForm
from .models import GroupChatRoom

class GroupChatRoomForm(ModelForm):
    class Meta:
        model= GroupChatRoom
        fields = ['name', 'topic', 'description']