# Generated by Django 4.1.7 on 2023-03-14 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competicion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='competicion',
            name='tabla',
            field=models.JSONField(default=[]),
        ),
    ]
