# Generated by Django 3.2 on 2022-04-04 14:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ietimoodle', '0005_merge_20220330_1915'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ejercicio',
            name='minVersion',
        ),
        migrations.RemoveField(
            model_name='ejercicio',
            name='ponderacion',
        ),
        migrations.RemoveField(
            model_name='ejercicio',
            name='visibilidad',
        ),
        migrations.RemoveField(
            model_name='entrega',
            name='comentario_alumno',
        ),
        migrations.RemoveField(
            model_name='entrega',
            name='comentario_profesor',
        ),
        migrations.RemoveField(
            model_name='entrega',
            name='cualificacion',
        ),
        migrations.RemoveField(
            model_name='entrega',
            name='cualificado',
        ),
        migrations.RemoveField(
            model_name='entrega',
            name='ejercicio',
        ),
        migrations.AddField(
            model_name='ejercicio',
            name='descripcion',
            field=models.CharField(default='pepe', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ejercicio',
            name='nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='entrega',
            name='archivo',
            field=models.FileField(blank=True, upload_to='./archivos/entregas/'),
        ),
        migrations.CreateModel(
            name='VRTarea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minversion', models.CharField(blank=True, max_length=255, null=True)),
                ('autograde', models.CharField(blank=True, max_length=255, null=True)),
                ('version', models.CharField(blank=True, max_length=255, null=True)),
                ('performance_data', models.CharField(blank=True, max_length=255, null=True)),
                ('ejercicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ietimoodle.ejercicio')),
            ],
        ),
        migrations.CreateModel(
            name='Tarea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('ponderacion', models.IntegerField(default=0)),
                ('visibilidad', models.BooleanField(default=False)),
                ('minVersion', models.CharField(blank=True, max_length=200, null=True)),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ietimoodle.curso')),
                ('ejercicio', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='ietimoodle.ejercicio')),
            ],
        ),
        migrations.CreateModel(
            name='Calificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', models.IntegerField(null=True)),
                ('fecha_entrega', models.DateTimeField()),
                ('comentario_profesor', models.CharField(blank=True, max_length=255, null=True)),
                ('comentario_alumno', models.CharField(blank=True, max_length=255, null=True)),
                ('tarea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ietimoodle.tarea')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='entrega',
            name='tarea',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ietimoodle.tarea'),
        ),
        migrations.AddField(
            model_name='entrega',
            name='vrtarea',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ietimoodle.vrtarea'),
        ),
    ]