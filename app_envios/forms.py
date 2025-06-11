
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Cliente

class RegistroClienteForm(UserCreationForm):
    direccion = forms.CharField(max_length=255)

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'tipo': forms.HiddenInput()  # Auto-set to 'cliente'
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['tipo'].initial = 'cliente'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.tipo = 'cliente'
        if commit:
            user.save()
            Cliente.objects.create(user=user, direccion=self.cleaned_data['direccion'])
        return user

