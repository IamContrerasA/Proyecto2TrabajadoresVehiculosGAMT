# Generated by Django 3.1.1 on 2020-10-16 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('CheckListApp', '0001_initial'),
        ('TrabajadoresApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='checklist',
            name='worker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='TrabajadoresApp.worker'),
        ),
    ]
