# Generated by Django 3.2 on 2022-04-01 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ietimoodle', '0006_auto_20220401_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrega',
            name='pin',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]