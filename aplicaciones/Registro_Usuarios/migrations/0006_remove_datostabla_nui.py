# Generated by Django 5.1.1 on 2024-10-04 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Registro_Usuarios', '0005_alter_datostabla_peso_l_alter_datostabla_valor_peso'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datostabla',
            name='nui',
        ),
    ]
