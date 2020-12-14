"""Proyecto2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin  
from django.urls import path, include  
from django.conf import settings
from django.conf.urls.static import static 

if settings.DEBUG == True:
    static_root_path = settings.STATICFILES_DIRS
elif settings.DEBUG == False:
    static_root_path = settings.STATIC_ROOT

urlpatterns = [  
    path('admin/', admin.site.urls), 
    path('', include('BaseApp.urls')),
    path('workers/', include('TrabajadoresApp.urls')),
    path('vehicles/', include('VehiculosApp.urls')),
    path('areas/', include('AreasApp.urls')),
    path('fatigues/', include('FatigasApp.urls')),
    path('users/', include('UsuariosApp.urls')),
    path('check_lists/', include('CheckListApp.urls')),
    path('companies/', include('EmpresasApp.urls')),
    path('excel/', include('ExcelApp.urls')),
    path('reports/', include('ReportesApp.urls')),
    
] + static(settings.STATIC_URL, document_root = static_root_path)

