# Generated by Django 3.1.1 on 2020-11-02 03:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ExcelApp', '0015_observaciones'),
    ]

    operations = [
        migrations.AddField(
            model_name='observaciones',
            name='descripcion',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='observaciones',
            name='estado',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='ExcelApp.estado'),
        ),
        migrations.AddField(
            model_name='observaciones',
            name='evidencia',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='observaciones',
            name='evidencia_correctiva',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='observaciones',
            name='accion_plan',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
