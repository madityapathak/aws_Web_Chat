from django.urls import path
from . import views


app_name = 'notifications'

urlpatterns = [
    path("",views.notification_page,name="notification"),
    path("delete/",views.delete_notification,name="delete-notification"),
    path('clear/all/',views.delete_all_notifications,name='delete-all-notifications'),
    path('seen/',views.seen_status,name="seen-status"),
]


