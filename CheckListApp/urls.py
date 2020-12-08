from django.urls import path  

from CheckListApp import views

urlpatterns = [  
    path('create', views.create),  
    path('index',views.index, name="CheckListIndex"),  
    
    path('show/<int:id>', views.show),  
    path('edit/<int:id>', views.edit),  
    path('update/<int:id>', views.update),  
    path('delete/<int:id>', views.destroy),   
    
] 
