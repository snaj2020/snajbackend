from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from . import views

#router = routers.DefaultRouter()
#router.register(r'procedimiento',views.getProcedimiento,basename='procedimiento')

urlpatterns =[
                path('getProcedimientoCodigo/<str:codProc>',views.getProcedimientoCodigo),
                path('getProcedimientoNombre/<str:nombreProc>',views.getProcedimientoNombre),
                path('getProcedimientoNombreIgual/<str:nombreProc>',views.getProcedimientoNombreIgual),
                path('getDocumentosProc/<str:codProc>/<int:idMod>',views.getDocumentosProc),
                path('getMaterialesProc/<str:codProc>/<int:idMod>',views.getMaterialesProc),
                path('getEquiposProc/<str:codProc>/<int:idMod>',views.getEquiposProc),
                path('getEspecialidadesProc/<str:codProc>/<int:idMod>',views.getEspecialidadesProc),
                path('listAllProcedimientos',views.listAllProcedimientos),
                path('listAllModalidades',views.listAllModalidades),
                path('addProcedimiento',views.addProcedimiento),
                path('deleteProcedimiento/<str:codProc>',views.deleteProcedimiento),
                path('getTiposProc',views.getTiposProc)
                
                
                
                #path(r'^api/', include(router.urls)),
    	        #path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
            ]

