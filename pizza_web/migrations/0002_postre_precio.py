# Generated by Django 4.0.4 on 2022-06-04 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='postre',
            name='precio',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
