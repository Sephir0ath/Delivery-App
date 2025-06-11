from django.shortcuts import render, redirect
from .forms import RegistroClienteForm, RegistroConductorForm, CustomLoginForm
from .models import  Usuario, Conductor, Cliente
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm  # O tu CustomLoginForm
from .forms import CustomLoginForm  # Asegúrate que este hereda de AuthenticationForm


def register_cliente(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  # o donde quieras redirigir
    else:
        form = RegistroClienteForm()
    return render(request, 'register_cliente.html', {'form': form})


def register_conductor(request):
    if request.method == 'POST':
        form = RegistroConductorForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('conductor_dashboard')
    else:
        form = RegistroConductorForm()
    return render(request, 'register_conductor.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Redirección por tipo
            if user.tipo == 'cliente':
                return redirect('home')
            elif user.tipo == 'conductor':
                return redirect('home')
            elif user.tipo == 'despachador':
                return redirect('home')
            elif user.tipo == 'admin':
                return redirect('admin_dashboard')
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})
