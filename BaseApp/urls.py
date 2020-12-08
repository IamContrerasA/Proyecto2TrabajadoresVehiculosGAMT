from django.urls import path, include  

from BaseApp import views

urlpatterns = [  
   
    path('base',views.base),      
    path('',views.welcome, name="Welcome"),  
    path('save_index',views.save_index),      
    
    
    path('signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),    
] 
