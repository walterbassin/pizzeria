# Generated by Django 4.0.4 on 2022-07-02 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_web', '0005_rename_image_pizza_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pizza',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='pizzas'),
        ),
    ]
