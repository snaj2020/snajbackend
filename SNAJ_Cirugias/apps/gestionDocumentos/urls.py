from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from . import views

#router = routers.DefaultRouter()
#router.register(r'procedimiento',views.getProcedimiento,basename='procedimiento')

urlpatterns =[
                path('addDocumentoAdjunto',views.addDocumentoAdjunto),
                path('editDocumentoAdjunto',views.editDocumentoAdjunto),
                path('deleteDocumentoAdjunto/<int:idDocAdj>',views.deleteDocumentoAdjunto),
                path('getEstadosDocAjunto',views.getEstadosDocAjunto),
                path('listDocAdjunto/<int:idAgenProc>',views.listDocAdjunto),
                path('getArchivoAdjunto/<int:idDocAdj>',views.getArchivoAdjunto),
                path('getAllDocumentos',views.getAllDocumentos)
                
                #path(r'^api/', include(router.urls)),
    	        #path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
            ]