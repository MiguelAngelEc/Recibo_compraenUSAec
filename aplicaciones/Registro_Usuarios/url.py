from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='gestionUsuarios'),
    path('facturaUsuarios/', views.facturaUsuarios, name='facturaUsuarios'),
    #URL para registrar Tiendas
    path('registrarTiendas/', views.registrarTiendas, name='registrarTiendas'),
    #URL buscar clientes en Factura
    path('buscar_usuario/', views.buscarUsuarios, name='buscarUsuarios'),
    #URL para enviar datos 
    path('guardar_datos/', views.guardar_datos, name='guardar_datos'),
    #URL para agregar usuarios
    path('registrarUsuarios/', views.registrarUsuarios),
    #URL para editar cursos
    path('edicionUsuarios/<codigo>', views.edicionUsuarios),
    #URL que muestra editarUsuarios.html
    path('editarUsuarios/', views.editarUsuarios),
    #URL para eliminar usuaiors
    path('eliminarUsuarios/<codigo>', views.eliminarUsuarios)
]