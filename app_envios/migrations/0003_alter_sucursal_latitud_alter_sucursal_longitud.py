# Generated by Django 5.2.1 on 2025-06-11 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_envios', '0002_alter_paquete_viaje'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sucursal',
            name='latitud',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='sucursal',
            name='longitud',
            field=models.FloatField(),
        ),
    ]
