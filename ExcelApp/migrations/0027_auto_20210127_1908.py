# Generated by Django 3.1.1 on 2021-01-28 00:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ExcelApp', '0026_auto_20210127_1700'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fotosobservaciones',
            old_name='obervacion',
            new_name='observacion',
        ),
    ]
