from django import forms
from django.contrib.auth.forms import AuthenticationForm
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

class RegistroClienteForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput,
        strip=False
    )
    password2 = forms.CharField(
        label='Repetir contraseña',
        widget=forms.PasswordInput,
        strip=False
    )
    direccion = forms.CharField(label='Dirección', max_length=255)

    class Meta:
        model = Usuario
        fields = ['username']  # username será tratado como email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Correo electrónico'
        self.fields['username'].widget.attrs.update({'placeholder': 'correo@ejemplo.com'})

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data['username']
        user.username = email
        user.email = email
        user.set_password(self.cleaned_data['password1'])
        user.tipo = 'cliente'
        if commit:
            user.save()
            Cliente.objects.create(user=user, direccion=self.cleaned_data['direccion'])
        return user


# -------------------------
# Registro de conductores
# -------------------------
class RegistroConductorForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    licencia = forms.CharField(max_length=50)

    class Meta:
        model = Usuario
        fields = ['username', 'password']  # 'username' será el email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Correo electrónico'
        self.fields['username'].widget.attrs.update({'placeholder': 'correo@ejemplo.com'})

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data['username']
        user.username = email
        user.email = email
        user.set_password(self.cleaned_data['password'])
        user.tipo = 'conductor'
        if commit:
            user.save()
            Conductor.objects.create(user=user, licencia=self.cleaned_data['licencia'])
        return user
