# Generated by Django 3.2 on 2022-03-25 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ietimoodle', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrega',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='./archivos/entregas/'),
        ),
        migrations.AlterField(
            model_name='entrega',
            name='comentario_alumno',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='entrega',
            name='comentario_profesor',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='entrega',
            name='cualificacion',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
