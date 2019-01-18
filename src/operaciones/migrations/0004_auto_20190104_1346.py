# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-01-04 13:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operaciones', '0003_historicalsoportemantenimiento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operacion',
            name='proveedor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proveedores.Proveedor'),
        ),
    ]