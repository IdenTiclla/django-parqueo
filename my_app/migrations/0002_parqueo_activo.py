# Generated by Django 3.2.9 on 2021-12-21 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='parqueo',
            name='activo',
            field=models.BooleanField(default=True),
        ),
    ]