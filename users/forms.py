from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class CreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('name', 'username', 'email')
