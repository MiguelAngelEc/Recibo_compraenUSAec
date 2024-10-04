from django.shortcuts import render, redirect
from decimal import Decimal, InvalidOperation
import logging
from .models import Usuarios, DatosTabla 
from .forms import TiendaForm
from django.contrib import messages



logger = logging.getLogger(__name__)
# Create your views here.

def home(request):
    usuariosListados = Usuarios.objects.all()
    return render(request, "gestionUsuarios.html", {"usuarios": usuariosListados}) 

#Funcion que permite Agregrar Usuarios
def registrarUsuarios(request):
    if request.method == 'POST':
        cedula=request.POST['txtCedula']
        nombre=request.POST['txtNombre']
        telefono=request.POST['txtTelefono']
        direccion=request.POST['txtDireccion']
        ciudad=request.POST['txtCiudad']
        email=request.POST['txtEmail']
        if Usuarios.objects.filter(cedula=cedula).exists():
            messages.error(request, 'La cédula ya está registrada.')
            return redirect('/')
    
        Usuarios.objects.create(cedula=cedula, nombre=nombre, telefono=telefono, direccion=direccion, ciudad=ciudad, email=email,)
        messages.success(request, 'Usuario Registrado!!')
        return redirect('/')
    else:
        return redirect('/')
   
#Funcion para editar Usuarios
def edicionUsuarios(request, codigo):
    try:
        usuarios = Usuarios.objects.get(cedula=codigo)
        return render(request, "edicionUsuarios.html", {"usuarios": usuarios})
    except Usuarios.DoesNotExist:
        messages.error(request, 'Usuario no encontrado')
        return redirect('/')


#Funcion para mostrar editarUsuarios.html
def editarUsuarios(request):
    cedula=request.POST['txtCedula']
    nombre=request.POST['txtNombre']
    telefono=request.POST['txtTelefono']
    direccion=request.POST['txtDireccion']
    ciudad=request.POST['txtCiudad']
    email=request.POST['txtEmail']
    
    usuarios = Usuarios.objects.get(cedula=cedula)
    
    usuarios.nombre = nombre
    usuarios.telefono = telefono
    usuarios.direccion = direccion
    usuarios.ciudad = ciudad
    usuarios.email = email
    usuarios.save()
    
    
    messages.success(request, 'Usuario Actualizado!!')
    return redirect ('/')

# Funcion que permite eliminar Usuarios
def eliminarUsuarios(request, codigo):
    usuarios = Usuarios.objects.get(cedula=codigo)
    usuarios.delete() 
    messages.success(request, 'Usuario Eliminado!!')
    return redirect('/')

#Parte de Factura
#Busca con numero de cedula 
# def facturaUsuarios(request):
#     usuarios = None
#     if request.method == 'POST':
#         # Obtener la cédula ingresada en el formulario
#         cedula = request.POST.get('cedula')

#         # Verificar si se ingresó una cédula y buscar en la base de datos
#         if cedula:
#             usuarios = Usuarios.objects.filter(cedula=cedula)
#         else:
#             usuarios = Usuarios.objects.none()  # No mostrar nada si no hay cédula
#     else:
#         usuarios = Usuarios.objects.none()  # Si no es POST, no mostrar usuarios

#     return render(request, 'facturaUsuarios.html', {'usuarios': usuarios})   

#Parte para el Valor de las Facturas
#Tabla para mostrar los valores
def facturaUsuarios(request):
    
    usuarios = None  # Cambio de nombre para no sobrescribir el modelo
    form = TiendaForm()
    tiendas = DatosTabla.objects.all()

    total_general_peso = Decimal('0.0')
    total_flete = Decimal('0.0')
    total_isd = Decimal('0.0')
    total_final = Decimal('0.0')

    # Calcular los totales
    for tienda in tiendas:
        tienda.titulo = tienda.titulo if tienda.titulo else 'S/D'
        tienda.wr = tienda.wr if tienda.wr else 'S/D'
        tienda.peso_l = tienda.peso_l if tienda.peso_l is not None else Decimal('0.0')
        tienda.valor_peso = tienda.valor_peso if tienda.valor_peso is not None else Decimal('0.0')
        tienda.total_peso = tienda.total_peso if tienda.total_peso is not None else Decimal('0.0')

        total_general_peso += tienda.total_peso
        total_flete += tienda.flete if tienda.flete else Decimal('0.0')
        total_isd += tienda.ISD if tienda.ISD else Decimal('0.0')

    # Calcular el total final
    total_final = total_general_peso + total_flete + total_isd

    if request.method == 'POST':
        # Si se envía el formulario para guardar una tienda
        if 'submit_tienda' in request.POST:
            form = TiendaForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('facturaUsuarios')

        # Si se busca un usuario por cédula
        elif 'submit_buscar' in request.POST:
    # Procesar el formulario de búsqueda de cédula
            cedula = request.POST.get('cedula')
            if cedula:
                usuarios = Usuarios.objects.filter(cedula=cedula)
            else:
                usuarios = Usuarios.objects.none()

        # Si se elimina todo el contenido de la tabla
        elif 'submit_eliminar_todos' in request.POST:
            DatosTabla.objects.all().delete()

    # Renderizamos la plantilla con los datos necesarios
    return render(request, 'facturaUsuarios.html', {
        'form': form,
        'tiendas': tiendas,
        'total_general_peso': total_general_peso,
        'total_flete': total_flete,
        'total_isd': total_isd,
        'total_final': total_final,  # Total final
        'usuario_resultado': usuarios  # Pasamos la variable al contexto
    })

#funcion que elimina los valores
def eliminar_todos_los_registros(request):
    if request.method == 'POST':
        # Eliminar todos los registros de DatosTabla
        DatosTabla.objects.all().delete()
        # Redirigir a otra vista (puedes cambiar la URL a donde desees)
        return redirect('facturaUsuarios')

    


