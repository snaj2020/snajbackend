from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from . import views

#router = routers.DefaultRouter()
#router.register(r'procedimiento',views.getProcedimiento,basename='procedimiento')

urlpatterns =[
                path('addAgendaMaterial',views.addAgendaMaterial),
                path('editAgendaMaterial',views.editAgendaMaterial),
                path('deleteAgendaMaterial/<int:idAgenMat>',views.deleteAgendaMaterial),
                path('getEstadosAgendaMat',views.getEstadosAgendaMat),
                path('listAgendaMaterial/<int:idAgenProc>',views.listAgendaMaterial),
                path('getAllMateriales',views.getAllMateriales)
                #path(r'^api/', include(router.urls)),
    	        #path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
            ]