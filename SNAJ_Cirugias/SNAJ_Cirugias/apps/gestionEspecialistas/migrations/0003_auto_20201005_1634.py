# Generated by Django 3.1.1 on 2020-10-05 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionEspecialistas', '0002_auto_20201001_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='especialidad',
            name='nombre',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='especialista',
            name='registroMedico',
            field=models.CharField(max_length=20),
        ),
    ]
