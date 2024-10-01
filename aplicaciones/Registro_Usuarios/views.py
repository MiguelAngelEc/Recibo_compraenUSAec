from django.shortcuts import render, redirect
from .models import Usuarios, Tiendas, DatosTabla
from django.contrib import messages

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
    else:
        return redirect('/')

#Funcion para editar cursos
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

#Plantilla FACTURASUAURIOS.HTML
def facturaUsuarios(request):
    tiendasListadas = Tiendas.objects.all()
    return render(request, "facturaUsuarios.html", {"tiendas":tiendasListadas})  

def registrarTiendas(request):
    if request.method == 'POST':
        nombre = request.POST['txtTienda']
        
        # Verificar si la tienda ya existe
        if Tiendas.objects.filter(nombre=nombre).exists():
            messages.error(request, 'La tienda ya está registrada.')
            # Renderiza la misma página con el mensaje de error
            return render(request, 'facturaUsuarios.html', {"tiendas": Tiendas.objects.all()})

        # Si no existe, crea la nueva tienda
        Tiendas.objects.create(nombre=nombre)
        messages.success(request, 'Tienda registrada exitosamente.')

    # Si no es un POST o después de registrar la tienda, renderiza la página
    return render(request, 'facturaUsuarios.html', {"tiendas": Tiendas.objects.all()})

def buscarUsuarios(request):
    if request.method == 'POST':
        cedula = request.POST['txtCedula']

        # try:
        #     usuario = Usuarios.objects.get(cedula=cedula)
        #     # Aquí se retornarán los datos del usuario a la página donde se mostrará el formulario
        #     return render(request, 'facturaUsuarios.html', {'usuario': usuario})
        # except Usuarios.DoesNotExist:
        #     # Si no encuentra al usuario, puedes manejar el error
        #     messages.error(request, 'Usuario no encontrado!')
        #     return render(request, 'facturaUsuarios.html')  # Redirige a una página principal o al mismo formulario
        try:
            usuario = Usuarios.objects.get(cedula=cedula)
            
            if request.is_ajax():  # Verifica si la petición es AJAX
                html = render_to_string('usuario_parcial.html', {'usuario': usuario})
                return JsonResponse({'facturaUsuarios.html': facturaUsuarios.html})
            else:
                # Si no es AJAX, renderiza la página completa
                return render(request, 'facturaUsuarios.html', {'usuario': usuario})
        
        except Usuarios.DoesNotExist:
            if request.is_ajax():
                return JsonResponse({'facturaUsuarios.html': '<p style="color:red;">Usuario no encontrado!</p>'})
            else:
                messages.error(request, 'Usuario no encontrado!')
                return render(request, 'facturaUsuarios.html')
        
# Crea un a interaccion con la base de datos para crear y enviar a los campos correspondietes
def guardar_datos(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        tienda = request.POST['tienda']
        wr = request.POST['wr']
        tkr_id = request.POST['tkr_id']
        abono = request.POST['abono']
        precio = request.POST['precio']
        subtotal = request.POST['subtotal']
        peso = request.POST['peso']
        valor_peso = request.POST['valor_peso']
        total_peso = request.POST['total_peso']
        
        # Crear un nuevo objeto de tu modelo y guardar los datos
        nuevo_dato = DatosTabla(
            tienda=tienda,
            wr=wr,
            tkr_id=tkr_id,
            abono=abono,
            precio=precio,
            subtotal=subtotal,
            peso=peso,
            valor_peso=valor_peso,
            total_peso=total_peso
        )
        nuevo_dato.save()  # Guardar en la base de datos

        # Redirigir después de guardar (puedes cambiar a otra URL si es necesario)
        return redirect('guardar_datos')
    
    # Si es una solicitud GET, mostrar la tabla con los datos guardados
    datos = DatosTabla.objects.all()
    return render(request, 'facturaUsuarios.html', {'datos': datos})
