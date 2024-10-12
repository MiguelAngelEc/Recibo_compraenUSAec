from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #Funcion de fecha
    path('', views.home, name='gestionUsuarios'),
    #URL de Imprimir
    path('reciboImprimir/', views.reciboImprimir, name='reciboImprimir'),
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
    #Elimina los valores de la Factura
    path('eliminar-todos/', views.eliminar_todos_los_registros, name='eliminar_todos_los_registros'),

    #Generar PDF
    path('factura/pdf/', views.factura_pdf, name='factura_pdf'),

   
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)