from django.urls import path  

from ExcelApp import views

from Proyecto2 import settings
from django.conf.urls.static import static

urlpatterns = [  

    path('create', views.create),  
    path('index',views.index, name="ExcelIndex"),    
           
    path('db/<int:id>', views.db),
    path('db/edit/<int:id>', views.edit),  
    path('db/update/<int:id>', views.update),  
    path('db/delete/<int:id>', views.destroy),
    
    path('db/<int:id>/fatiga_modal/<int:id2>',views.fatiga_modal),
    path('db/<int:id>/declaracion_modal/<int:id2>',views.declaracion_modal),
    path('db/<int:id>/iperc_modal/<int:id2>',views.iperc_modal),
    path('db/<int:id>/checklist_modal/<int:id2>',views.checklist_modal),
    path('db/<int:id>/show_driver/<int:id2>',views.show_driver),
    path('db/<int:id>/show_vehicle/<int:id2>/<int:id3>',views.show_vehicle),
    path('db/<int:id>/obs/<int:id2>',views.obs),    
    path('db/<int:id>/obs_update/<int:id2>/<int:id3>',views.obs_update),
    path('db/<int:id>/obs_aprove/<int:id2>/<int:id3>',views.obs_aprove),
    path('db/<int:id>/obs_disaprove/<int:id2>/<int:id3>',views.obs_disaprove),

    path('db/obs_camera/<int:id>',views.obs_camera),
    path('db/image_editor/<int:id>', views.image_editor), 
    path('db/update_image_editor/<int:id>', views.update_image_editor), 

    path('db/take_photo_vehicle/<int:id>', views.take_photo_vehicle),
    path('db/download_photos_v/<str:id>', views.download_photos_v), 
    path('db/add_disinfect', views.add_disinfect), 
    
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
