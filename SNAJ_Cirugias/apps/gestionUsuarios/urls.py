from django.urls import include, path
from rest_framework import routers
from . import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('addUser', views.addUser),
    path('getUser/<str:username>', views.getUser),
    path('getUserConId/<int:idUser>', views.getUserConId),
    path('deleteUser/<str:username>', views.deleteUser),
    path('listActiveUsers', views.listActiveUsers),
    path('editUserAdmin',views.editUserAdmin),
    path('editUserUser',views.editUserUser),
    path('changePasswordUser',views.changePasswordUser),
    path('changePasswordAdmin',views.changePasswordAdmin),
    path('logout',views.logout),
    path('getUserGroupWithToken',views.getUserGroupWithToken),
    path('getGroups',views.getGroups),
    path('resetPassword/<str:toEmail>',views.resetPassword),
    path('login',views.login)
]