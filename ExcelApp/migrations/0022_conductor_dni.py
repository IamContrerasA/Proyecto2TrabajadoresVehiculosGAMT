# Generated by Django 3.1.1 on 2020-12-07 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ExcelApp', '0021_auto_20201202_2045'),
    ]

    operations = [
        migrations.AddField(
            model_name='conductor',
            name='dni',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
