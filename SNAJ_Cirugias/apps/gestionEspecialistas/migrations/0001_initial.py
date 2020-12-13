# Generated by Django 3.1.1 on 2020-10-01 23:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('agendamiento', '0001_initial'),
        ('gestionPacientes', '0001_initial'),
        ('gestionProcedimientos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Especialidad',
            fields=[
                ('codigoEspecialidad', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Especialista',
            fields=[
                ('idEspecialista', models.AutoField(primary_key=True, serialize=False)),
                ('registroMedico', models.CharField(max_length=15)),
                ('idPersona', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='gestionPacientes.persona')),
            ],
        ),
        migrations.CreateModel(
            name='EspecialidadRequerida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('codigoEspecialidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionEspecialistas.especialidad')),
                ('idProcedimientoModalidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionProcedimientos.procedimientomodalidad')),
            ],
        ),
        migrations.CreateModel(
            name='AgendaEspecialista',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('PEND', 'Pendiente'), ('AGEN', 'Agendado')], default=('PEND', 'Pendiente'), max_length=15)),
                ('idAgendaProcedimiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agendamiento.agendaprocedimiento')),
                ('idEspecialista', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionEspecialistas.especialista')),
            ],
        ),
    ]