from django import forms
from django.contrib.auth.models import User
from baseapp.models import Table


class user_info_Forms(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    class Meta():
        model = User
        fields = ('username', 'email', 'password')
        help_texts = {
            'username': None,
        }

class work_info_forms(forms.ModelForm):
    
    class Meta():
        model=Table
        fields = ('user','title', 'desc','Datetime')
