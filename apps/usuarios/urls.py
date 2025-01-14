
from django.urls import include, path
from . import views
from .views import (
    login_view,
    logout_view,
    dashboard_view,
    coordinador_dashboard,
    asesor_dashboard,
    aprendiz_dashboard,
)
from django.contrib.auth import views as auth_view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required


urlpatterns = [
    #auth
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    #dashboard
    path('dashboard/', dashboard_view, name='dashboard'),

    # dashboards peer rol
    path('coordinador/dashboard/', coordinador_dashboard, name='coordinador_dashboard'),
    path('asesor/dashboard/', asesor_dashboard, name='asesor_dashboard'),
    path('aprendiz/dashboard/', aprendiz_dashboard, name='aprendiz_dashboard'),
    # path('verification/', include('verify_email')),

    #procesar excel
    #path('procesar_excel/', views.procesar_excel, name='procesar_excel'),
    #path('cargar-usuarios/', views.cargar_usuarios, name='cargar_usuarios'),
    path('cargar-aprendices/', views.cargar_aprendices, name='cargar_aprendices'),
]

