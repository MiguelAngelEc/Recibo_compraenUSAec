from django.shortcuts import render, redirect
from .models import Usuarios
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
def facturaUsuarios(request):
    usuario = None
    if request.method == 'POST':
        # Obtener la cédula ingresada en el formulario
        cedula = request.POST.get('cedula')

        # Verificar si se ingresó una cédula y buscar en la base de datos
        if cedula:
            usuarios = Usuarios.objects.filter(cedula=cedula)
        else:
            usuarios = Usuarios.objects.none()  # No mostrar nada si no hay cédula
    else:
        usuarios = Usuarios.objects.none()  # Si no es POST, no mostrar usuarios

    return render(request, 'facturaUsuarios.html', {'usuarios': usuarios})   



