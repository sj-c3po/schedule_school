from django.forms import ModelForm  # форма, привязанная к модели
from schedule.models import Administration

class AutorizForm(ModelForm):
    class Meta:
        model = Administration
        fields = ['login', 'password']