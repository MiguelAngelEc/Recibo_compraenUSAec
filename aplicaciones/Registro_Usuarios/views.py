from django.shortcuts import render, redirect
from decimal import Decimal
import logging
from .models import Usuarios, DatosTabla 
from .forms import TiendaForm
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from io import BytesIO
from django.templatetags.static import static




logger = logging.getLogger(__name__)
# Create your views here.

def home(request):
    usuariosListados = Usuarios.objects.all()
    return render(request, "gestionUsuarios.html", {"usuarios": usuariosListados}) 

def reciboImprimir(request):
    return render(request, 'reciboImprimir.html')

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

#Parte para el Valor de las Facturas
#Tabla para mostrar los valores
def facturaUsuarios(request):
    usuarios = None  # Cambiar el nombre para no sobrescribir el modelo
    form = TiendaForm()
    tiendas = DatosTabla.objects.all()

    # Inicializar los totales
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
            cedula = request.POST.get('cedula')
            if cedula:
                usuarios = Usuarios.objects.filter(cedula=cedula)
            else:
                usuarios = Usuarios.objects.none()

        # Si se elimina todo el contenido de la tabla
        elif 'submit_eliminar_todos' in request.POST:
            DatosTabla.objects.all().delete() 
    
     # Renderizar la plantilla con los datos necesarios
    return render(request, 'facturaUsuarios.html', {
        'form': form,
        'tiendas': tiendas,
        'total_general_peso': total_general_peso,
        'total_flete': total_flete,
        'total_isd': total_isd,
        'total_final': total_final,
        'usuario_resultado': usuarios
    })

#funcion que elimina los valores
def eliminar_todos_los_registros(request):
    if request.method == 'POST':
        # Eliminar todos los registros de DatosTabla
        DatosTabla.objects.all().delete()
        # Redirigir a otra vista (puedes cambiar la URL a donde desees)
        return redirect('facturaUsuarios')

# Función para generar vista para PDF
def factura_pdf(request):
    tiendas = DatosTabla.objects.all()

    # Inicializar los totales
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

    # Renderizar la plantilla como HTML
    html_string = render_to_string('reciboImprimir.html', {
        'tiendas': tiendas,
        'total_general_peso': total_general_peso,
        'total_flete': total_flete,
        'total_isd': total_isd,
        'total_final': total_final
    })

    # Crear un objeto de BytesIO
    pdf_file = BytesIO()
    
    # Generar la ruta del archivo CSS
    css_path = static('css/recibo.css')

    # Convertir el HTML a PDF
    HTML(string=html_string).write_pdf(pdf_file)
   
    # Devolver el PDF como respuesta HTTP
    pdf_file.seek(0)
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="factura.pdf"'

    return response



    


