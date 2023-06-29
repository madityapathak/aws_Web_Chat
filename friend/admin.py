from django.contrib import admin
from .models import Friend_request,Friendlist
# Register your models here.
admin.site.register(Friendlist)
admin.site.register(Friend_request)