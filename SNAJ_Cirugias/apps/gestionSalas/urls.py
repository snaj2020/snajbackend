from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from . import views

#router = routers.DefaultRouter()
#router.register(r'procedimiento',views.getProcedimiento,basename='procedimiento')

urlpatterns =[
                path('getAllSalas',views.getAllSalas),
                path('getEstadosSalas',views.getEstadosSalas),
                path('getSalaConId/<int:idSal>',views.getSalaConId)
                
                
                
                
                #path(r'^api/', include(router.urls)),
    	        #path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
            ]

