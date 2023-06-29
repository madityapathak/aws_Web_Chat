from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserForm(UserCreationForm):
    class Meta:
        model= User
        fields = ['email','username','first_name','last_name']

class UpdateUserForm(ModelForm):
    class Meta:
        model= User
        fields = ['first_name','last_name','about']