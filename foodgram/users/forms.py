from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import User


class CreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('name', 'username', 'email')
