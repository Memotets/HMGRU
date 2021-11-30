from django import forms
from django.contrib.auth.forms import UserCreationForm
from authentication.models import Usuarios

class UsuariosForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def save(self, commit=True):
        usuario = super(UsuariosForm, self).save(commit=False)

        usuario.email = self.cleaned_data['email']
        
        if commit:
            usuario.save()
        
        return usuario

    class Meta:
        model = Usuarios
        fields = ('nombre', 'aPaterno', 'aMaterno', 'rfc', 'email')

class UsuariosEditForm(forms.ModelForm):

    def save(self, commit=True):
        usuario = super(UsuariosEditForm, self).save(commit=False)

        usuario.nombre = self.cleaned_data['nombre']
        usuario.aPaterno = self.cleaned_data['aPaterno']
        usuario.aMaterno = self.cleaned_data['aMaterno']
        usuario.email = self.cleaned_data['email']

        usuario.save()
        return usuario

    class Meta: 
        model = Usuarios
        fields = ('nombre', 'aPaterno', 'aMaterno', 'email')
