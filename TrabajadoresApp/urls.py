from django.urls import path  

from TrabajadoresApp import views

urlpatterns = [  
    path('emp', views.emp),  
    path('index',views.index, name="WorkerIndex"),  

    path('show/<int:id>', views.show),  
    path('edit/<int:id>', views.edit),  
    path('update/<int:id>', views.update),  
    path('delete/<int:id>', views.destroy),   

    path('<int:id>/results/create', views.r_create), 
    path('<int:id>/results/index',views.r_index),         

    path('<int:id>/results/show/<int:id2>', views.r_show),  
    path('<int:id>/results/edit/<int:id2>', views.r_edit),  
    path('<int:id>/results/update/<int:id2>', views.r_update),  
    path('<int:id>/results/delete/<int:id2>', views.r_destroy),   

    path('add_hours/create', views.wr_create), 
    path('result_hours/index',views.wr_index),         
    path('check_lists/create',views.wcl_create),


] 
