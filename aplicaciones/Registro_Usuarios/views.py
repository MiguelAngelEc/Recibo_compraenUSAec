from django.shortcuts import render, redirect
from decimal import Decimal
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
# #Busca con numero de cedula 
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
    usuarios = None
    form = TiendaForm()  # Asegurar que form siempre tenga un valor por defecto
    tiendas = DatosTabla.objects.all()  # Obtener todos los registros de DatosTabla

    # Si el campo es vacío, coloca 'S/D'
    for tienda in tiendas:
        tienda.titulo = tienda.titulo if tienda.titulo else 'S/D'
        tienda.wr = tienda.wr if tienda.wr else 'S/D'
        tienda.tkr = tienda.tkr if tienda.tkr else 'S/D'
        tienda.abono = tienda.abono if tienda.abono is not None else Decimal('0.0')
        tienda.precio = tienda.precio if tienda.precio is not None else Decimal('0.0')
        tienda.subtotal = tienda.subtotal if tienda.subtotal is not None else Decimal('0.0')
        tienda.peso_l = tienda.peso_l if tienda.peso_l is not None else Decimal('0.0')
        tienda.valor_peso = tienda.valor_peso if tienda.valor_peso is not None else Decimal('0.0')
        tienda.total_peso = tienda.total_peso if tienda.total_peso is not None else Decimal('0.0')

    # Sumar subtotales y total_peso de todas las filas
    total_general_subtotal = sum(tienda.subtotal for tienda in tiendas)
    total_general_peso = sum(tienda.total_peso for tienda in tiendas)
    total_suma = total_general_subtotal + total_general_peso  # Suma total

    total_final = total_suma  # Inicializa el total final

    if request.method == 'POST':
        if 'submit_tienda' in request.POST:
            # Procesar el formulario TiendaForm
            form = TiendaForm(request.POST)
            if form.is_valid():
                form.save()
                tiendas = DatosTabla.objects.all()
                total_general_subtotal = sum(tienda.subtotal for tienda in tiendas)
                total_general_peso = sum(tienda.total_peso for tienda in tiendas)
                total_suma = total_general_subtotal + total_general_peso

        elif 'submit_buscar' in request.POST:
            # Procesar el formulario de búsqueda de cédula
            cedula = request.POST.get('cedula')
            if cedula:
                usuarios = Usuarios.objects.filter(cedula=cedula)
            else:
                usuarios = Usuarios.objects.none()  # No mostrar nada si no hay cédula

        elif 'submit_eliminar_todos' in request.POST:
            # Procesar el formulario para eliminar todos los registros
            DatosTabla.objects.all().delete()

        # Obtener valores de Flete e ISD del formulario
        flete = request.POST.get('flete', 0)  # Valor por defecto 0 si no existe
        isd = request.POST.get('isd', 0)      # Valor por defecto 0 si no existe

        try:
            # Convertir a Decimal y calcular total final
            flete = Decimal(flete) if flete else Decimal('0.0')
            isd = Decimal(isd) if isd else Decimal('0.0')
        except (ValueError, InvalidOperation):
            flete = Decimal('0.0')
            isd = Decimal('0.0')

        total_final = total_suma + flete + isd  # Calcular total final

    # Renderiza la plantilla con los usuarios, el formulario y los datos de la tabla
    return render(request, 'facturaUsuarios.html', {
        'form': form,
        'usuarios': usuarios,
        'tiendas': tiendas,
        'total_general_subtotal': total_general_subtotal,
        'total_general_peso': total_general_peso,
        'total_suma': total_suma,
        'total_final': total_final  # Pasar total final al contexto
    })


#funcion que elimina los valores
def eliminar_todos_los_registros(request):
    if request.method == 'POST':
        # Eliminar todos los registros de DatosTabla
        DatosTabla.objects.all().delete()
        # Redirigir a otra vista (puedes cambiar la URL a donde desees)
        return redirect('facturaUsuarios')

    


