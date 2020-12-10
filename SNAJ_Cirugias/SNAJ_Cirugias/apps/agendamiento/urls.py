#region imports
from django.urls import path
from django.conf.urls import url
from . import views 

#endRegion

urlpatterns = [
    url('listAgendaProcedimiento',views.listAgendaProcedimiento),
    url('addAgendaProcedimiento',views.addAgendaProcedimiento),
    url('editAgendaProcedimiento',views.editAgendaProcedimiento),
    url('getEstadosAgendaProc',views.getEstadosAgendaProc),
    url('getEstadosCama',views.getEstadosCama),
    path('generateRecibido/<int:idAgendaProc>',views.generateRecibido),
    path('getAgendaProcsConFecha/<str:sinceDate>/<str:toDate>',views.getAgendaProcsConFecha),
    path('getAgendaProcConId/<int:idAgendaProc>',views.getAgendaProcConId),
    path('getAgendaProcsConIdenPac/<str:idenPac>',views.getAgendaProcsConIdenPac),
    path('validarEstadoAgenda/<int:idAgendaProcedimiento>',views.validarEstadoAgenda)
    
    #url(r'^api/agendaProcedimiento/(?P<pk>[0-9]+)$',views.AgendaProcedimientoDetail)
]


