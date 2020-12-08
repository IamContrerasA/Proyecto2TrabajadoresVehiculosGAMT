from django.urls import path  

from UsuariosApp import views

urlpatterns = [  
    path('create', views.create),  
    path('index',views.index, name="UserIndex"),  
    
    path('show/<int:id>', views.show),  
    path('edit/<int:id>', views.edit),  
    path('update/<int:id>', views.update),  
    path('delete/<int:id>', views.destroy), 

    path('edit_password/<int:id>', views.edit_password),  
    path('update_password/<int:id>', views.update_password),    
    
] 
