from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from .models import Cliente, Conductor

Usuario = get_user_model()

# -------------------------
# Formulario de login
# -------------------------
class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Correo electrónico'
        self.fields['username'].widget.attrs.update({'placeholder': 'correo@ejemplo.com'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Contraseña'})


# -------------------------
# Registro de clientes
# -------------------------

class RegistroClienteForm(UserCreationForm):
    direccion = forms.CharField(max_length=255)

    class Meta:
        model = Usuario
        fields = ['username', 'password1', 'password2']
        widgets = {
            'tipo': forms.HiddenInput()  # Auto-set to 'cliente'
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['tipo'].initial = 'cliente'
            self.fields['username'].label = 'Correo electrónico'
            self.fields['username'].widget.attrs.update({'placeholder': 'correo@ejemplo.com'})

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data['username']
        user.username = email
        user.email = user.username
        user.tipo = 'cliente'
        if commit:
            user.save()
            Cliente.objects.create(user=user, direccion=self.cleaned_data['direccion'])
        return user


# -------------------------
# Registro de conductores
# -------------------------
class RegistroConductorForm(UserCreationForm):
    licencia = forms.CharField(max_length=50)

    class Meta:
        model = Usuario
        fields = ['username', 'password1', 'password2']
        widgets = {
            'tipo': forms.HiddenInput()
        }  # 'username' será el email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo'].initial = 'conductor'
        self.fields['username'].label = 'Correo electrónico'
        self.fields['username'].widget.attrs.update({'placeholder': 'correo@ejemplo.com'})


    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data['username']
        user.username = email
        user.email = user.username
        user.tipo = 'conductor'
        if commit:
            user.save()
            Conductor.objects.create(user=user, licencia=self.cleaned_data['licencia'])
        return user
