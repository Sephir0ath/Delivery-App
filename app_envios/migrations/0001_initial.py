# Generated by Django 5.2.1 on 2025-06-10 23:43

import datetime
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_autenticacion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstadoEntrega',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comuna', models.CharField(max_length=50)),
                ('latitud', models.DecimalField(decimal_places=7, max_digits=10)),
                ('longitud', models.DecimalField(decimal_places=7, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Paquete',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_registro', models.DateField(default=datetime.date.today)),
                ('ancho', models.DecimalField(decimal_places=3, max_digits=7)),
                ('alto', models.DecimalField(decimal_places=3, max_digits=7)),
                ('largo', models.DecimalField(decimal_places=3, max_digits=7)),
                ('peso', models.DecimalField(decimal_places=2, max_digits=6)),
                ('destinatario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app_autenticacion.cliente')),
                ('estado_actual', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_envios.estadoentrega')),
                ('destino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_envios.sucursal')),
            ],
        ),
        migrations.CreateModel(
            name='HistorialPaquete',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(default=django.utils.timezone.now)),
                ('estado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_envios.estadoentrega')),
                ('paquete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_envios.paquete')),
            ],
        ),
        migrations.CreateModel(
            name='Viaje',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asignador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_autenticacion.despachador')),
                ('conductor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_autenticacion.conductor')),
                ('origen', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_envios.sucursal')),
            ],
        ),
        migrations.AddField(
            model_name='paquete',
            name='viaje',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_envios.viaje'),
        ),
    ]
