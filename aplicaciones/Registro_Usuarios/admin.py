from django.contrib import admin
from .models import Usuarios, Tiendas

# Register your models here.

admin.site.register(Usuarios)
admin.site.register(Tiendas)