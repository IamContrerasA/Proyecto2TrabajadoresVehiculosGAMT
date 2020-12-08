from django.urls import path  

from ReportesApp import views

urlpatterns = [  
    
    path('index',views.index, name="ReporteIndex"),  
    path('create',views.create),  
    path('generate_pdf',views.generate_pdf),  
        
] 