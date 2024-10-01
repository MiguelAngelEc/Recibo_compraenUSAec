from django.db import models

# Create your models here.

class Usuarios(models.Model):
    cedula = models.CharField(primary_key=True, max_length=15)
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=15)
    email = models.EmailField(max_length= 50)
    
    def __str__(self):
        texto = '{0} / {1} / {2}'
        return texto.format(self.cedula, self.nombre, self.ciudad)
    
class Tiendas(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class DatosTabla(models.Model):
    tienda = models.CharField(max_length=100)
    wr = models.CharField(max_length=100)
    tkr_id = models.CharField(max_length=100)
    abono = models.DecimalField(max_digits=10, decimal_places=2)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    peso = models.DecimalField(max_digits=10, decimal_places=2)
    valor_peso = models.DecimalField(max_digits=10, decimal_places=2)
    total_peso = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.tienda} - {self.wr}"