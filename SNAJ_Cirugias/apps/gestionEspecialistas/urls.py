from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from . import views

#router = routers.DefaultRouter()
#router.register(r'procedimiento',views.getProcedimiento,basename='procedimiento')

urlpatterns =[
                path('addAgendaEspecialista',views.addAgendaEspecialista),
                path('editAgendaEspecialista',views.editAgendaEspecialista),
                path('deleteAgendaEspecialista/<int:idAgenEsp>',views.deleteAgendaEspecialista),
                path('getEstadosEspecialistas',views.getEstadosEspecialistas),
                path('listAgendaEspecialistas/<int:idAgenProc>',views.listAgendaEspecialistas),
                path('getAllEspecialidades',views.getAllEspecialidades)
                #path(r'^api/', include(router.urls)),
    	        #path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
            ]