# Generated by Django 3.1.1 on 2020-10-01 23:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestionMateriales', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='agendamaterial',
            table='AgendaMaterial',
        ),
        migrations.AlterModelTable(
            name='material',
            table='Material',
        ),
        migrations.AlterModelTable(
            name='materialrequerido',
            table='MaterialRequerido',
        ),
    ]
