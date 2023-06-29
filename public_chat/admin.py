from django.contrib import admin
from .models import GroupMessage,GroupChatRoom
# Register your models here.
admin.site.register(GroupChatRoom)

admin.site.register(GroupMessage)