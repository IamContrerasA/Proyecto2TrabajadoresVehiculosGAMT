from django import forms  
from UsuariosApp.models import User, UserType
from django.contrib.auth.forms import UserCreationForm

class UserForm(forms.ModelForm):  
    class Meta:  
        model = User
        fields = "__all__"  
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs.update({'class': 'form-control'})

class UserCreateForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = UserType
        fields = UserCreationForm.Meta.fields + ('dni', 'role')
        widgets = {
            
        }