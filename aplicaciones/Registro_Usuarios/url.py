from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='gestionUsuarios'),
    # URL para editar usuarios
    path('edicionUsuarios/<codigo>/', views.edicionUsuarios, name='edicionUsuarios'),
    # Agrega la URL para registrar usuarios
    path('registrarUsuarios/', views.registrarUsuarios),
    # URL que muestra editarUsuarios.html
    path('editarUsuarios/', views.editarUsuarios, name='editarUsuarios'),
    # URL para eliminar usuarios
    path('eliminarUsuarios/<codigo>/', views.eliminarUsuarios, name='eliminarUsuarios'),
    # URL para factura de usuarios
    path('facturaUsuarios/', views.facturaUsuarios, name='facturaUsuarios'),
    #Crea vista de Busqueda de Usuario
  
]