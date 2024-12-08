from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .forms import CustomLoginForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
        return render(request, 'auth/login.html', {'form': form, 'error': 'Credenciales inválidas'})
    else:
        form = CustomLoginForm()
    return render(request, 'auth/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    if request.user.rol == 'coordinador':
        return redirect('coordinador_dashboard')
    elif request.user.rol == 'asesor':
        return redirect('asesor_dashboard')
    elif request.user.rol == 'aprendiz':
        return redirect('aprendiz_dashboard')
    else:
        return HttpResponse("No tienes un rol asignado.", status=403)


@login_required
def coordinador_dashboard(request):
    if request.user.rol == 'coordinador':
        return render(request, 'dashboards/coordinador_dashboard.html', {'user': request.user})
    else:
        return HttpResponse("Acceso denegado.", status=403)


@login_required
def asesor_dashboard(request):
    if request.user.rol == 'asesor':
        return render(request, 'dashboards/asesor_dashboard.html', {'user': request.user})
    else:
        return HttpResponse("Acceso denegado.", status=403)


@login_required
def aprendiz_dashboard(request):
    if request.user.rol == 'aprendiz':
        return render(request, 'dashboards/aprendiz_dashboard.html', {'user': request.user})
    else:
        return HttpResponse("Acceso denegado.", status=403)
