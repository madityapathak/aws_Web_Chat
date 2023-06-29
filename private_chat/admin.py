from django.contrib import admin
from .models import ChatRoom,Message
# Register your models here.
@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['id','participant1','participant2']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id','body','user']