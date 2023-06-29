from django.urls import path
from . import views


app_name = 'private_chat'

urlpatterns = [
    path('<str:pk>/',views.chat,name="chatroom"),
    path('delete/<str:pk>/',views.delete_a_message,name='delete-a-message'),
    path('chat/clear/',views.delete_conversation ,name='delete-conversation'),
    path('chat/unfreeze/',views.unfreeze_chat,name="unfreeze"),
    path('chat/freeze/',views.freeze_chat,name="freeze"),
    path('edit/message/',views.edit_message,name="edit-message"),
  
]


