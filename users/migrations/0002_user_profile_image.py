# Generated by Django 4.0.4 on 2022-07-02 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_profile',
            name='image',
            field=models.ImageField(default=1, upload_to='profile_image'),
            preserve_default=False,
        ),
    ]
