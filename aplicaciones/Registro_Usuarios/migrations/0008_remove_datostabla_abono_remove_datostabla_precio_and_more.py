# Generated by Django 5.1.1 on 2024-10-04 20:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Registro_Usuarios', '0007_datostabla_isd_datostabla_flete'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datostabla',
            name='abono',
        ),
        migrations.RemoveField(
            model_name='datostabla',
            name='precio',
        ),
        migrations.RemoveField(
            model_name='datostabla',
            name='subtotal',
        ),
    ]
