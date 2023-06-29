from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('',include('accounts.urls', namespace='accounts')),
    path('profile/',include('friend.urls', namespace='friend')),
    path('chat/',include('private_chat.urls', namespace='private_chat')),
    path('group-chat/',include('public_chat.urls', namespace='public_chat')),
    path('notifications/',include('notifications.urls', namespace='notifications')),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
