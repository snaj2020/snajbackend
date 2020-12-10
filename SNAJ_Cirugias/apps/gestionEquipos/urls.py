from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from . import views

#router = routers.DefaultRouter()
#router.register(r'procedimiento',views.getProcedimiento,basename='procedimiento')

urlpatterns =[
                path('addAgendaEquipo',views.addAgendaEquipo),
                path('editAgendaEquipo',views.editAgendaEquipo),
                path('deleteAgendaEquipo/<int:idEqu>',views.deleteAgendaEquipo),
                path('getEstadosAgendaEqu',views.getEstadosAgendaEqu),
                path('listAgendaEquipo/<int:idAgenProc>',views.listAgendaEquipo),
                path('getAllEquipos',views.getAllEquipos)

                #path(r'^api/', include(router.urls)),
    	        #path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
            ]