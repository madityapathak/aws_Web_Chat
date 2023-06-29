from django.urls import path
from . import views


app_name = 'friend'

urlpatterns = [
    path('<str:pk>/',views.profile,name="profile"),
    path('user/unfriend/',views.unfriend,name="unfriend"),
    path('user/cancle_request/',views.cancle_request,name="cancle-request"),
    path('user/send_request/',views.send_request,name="send-request"),
    path('user/accept/',views.accept,name="accept"),
    path('user/decline/',views.decline,name="decline"),
    path('<str:pk>/friend_list/',views.friend_list,name="friend-list"),
    path('sent/requests/',views.sent_requests_view,name='sent-requests'),
    path('recieved/requests/',views.recieved_requests_view,name='recieved-requests'),
    path('email/status/update/',views.email_status_view,name='email_status'),
   
]


