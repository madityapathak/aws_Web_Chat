from django.urls import path
from . import views


app_name = 'public_chat'

urlpatterns = [
    path("",views.home,name='home'),
    path('create/room/',views.create_room,name='create-room'),
    path('<str:pk>/',views.group_chat,name='chatroom'),
    path('delete/<str:pk>/',views.delete_a_message,name='delete-a-message'),
    path('edit/message/',views.edit_message,name="edit-message"),
    path('leave/room/',views.leave_room,name="leave-room"),
    path('chat/clear/',views.clear_convo,name="clear-convo"),
    path('chat/remove/',views.remove_user_from_group,name="remove-user"),
    path('chat/restrict/',views.restrict_message,name="restrict-message"),
    path('chat/unrestrict/',views.unrestrict_message,name="unrestrict-message"),
    path('delete/room/<str:pk>/',views.delete_room,name='delete-room'),
    path('update/<str:pk>/',views.update_room,name='update-room'),
    path('<room_id>/edit/cropImage/', views.crop_image, name="crop-image"),
    path('remove/roomImage/', views.remove_room_image, name="remove-room-image"),
]


