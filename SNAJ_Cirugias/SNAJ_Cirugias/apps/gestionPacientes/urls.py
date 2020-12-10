#region Imports
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from . import views
#endRegion



urlpatterns = [
    path('getPersonaIdentificacion/<str:idenPersona>',views.getPersonaIdentificacion),
    path('addPersona',views.addPersona),
    path('getTiposIdentificacion',views.getTiposIdentificacion)
]


