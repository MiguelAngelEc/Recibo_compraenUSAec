# Generated by Django 5.1.1 on 2024-10-04 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Registro_Usuarios', '0004_remove_datostabla_peso_remove_datostabla_tienda_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datostabla',
            name='peso_l',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='datostabla',
            name='valor_peso',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
    ]
