from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
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


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    if request.user.groups.filter(name='coordinador').exists():
        return redirect('coordinador_dashboard')
    elif request.user.groups.filter(name='asesor').exists():
        return redirect('asesor_dashboard')
    elif request.user.groups.filter(name='aprendiz').exists():
        return redirect('aprendiz_dashboard')
    else:
        return HttpResponse("No tienes un rol asignado.", status=403)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='coordinador').exists())
def coordinador_dashboard(request):
    return render(request, 'dashboards/coordinador_dashboard.html', {'user': request.user})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='asesor').exists())
def asesor_dashboard(request):
    return render(request, 'dashboards/asesor_dashboard.html', {'user': request.user})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='aprendiz').exists())
def aprendiz_dashboard(request):
    return render(request, 'dashboards/aprendiz_dashboard.html', {'user': request.user})
