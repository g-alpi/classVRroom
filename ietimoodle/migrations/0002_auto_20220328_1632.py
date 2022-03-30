# Generated by Django 3.2 on 2022-03-28 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ietimoodle', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrega',
            name='pin',
            field=models.IntegerField(blank=True, max_length=4, null=True),
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
    ]
