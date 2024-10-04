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

class DatosTabla(models.Model):           # Campo no obligatorio
    titulo = models.CharField(max_length=100, null=True, blank=True)        # Campo no obligatorio
    wr = models.CharField(max_length=50, null=True, blank=True)            # Campo no obligatorio
    tkr = models.CharField(max_length=50, null=True, blank=True)           # Campo no obligatorio
    abono = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Campo no obligatorio
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Campo no obligatorio
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Campo no obligatorio
    peso_l = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True) # Campo no obligatorio
    valor_peso = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)# Campo no obligatorio
    total_peso = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Campo no obligatorio
    
    def __str__(self):
        return f"{self.titulo} - {self.wr}"
    
    def save(self, *args, **kwargs):
        # Calculamos el total de peso
        if self.peso_l and self.valor_peso:
            self.total_peso = self.peso_l * self.valor_peso
        else:
            self.total_peso = 0
        
        # Calculamos el subtotal
        if self.precio and self.abono:
            self.subtotal = self.precio - self.abono
        else:
            self.subtotal = 0
        
        super().save(*args, **kwargs)
    
    def total_subtotal(self):
        subtotal = self.subtotal if self.subtotal else 0
        total_peso = self.total_peso if self.total_peso else 0
        return subtotal + total_peso
    
