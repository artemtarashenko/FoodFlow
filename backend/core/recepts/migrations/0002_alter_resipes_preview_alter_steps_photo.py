# Generated by Django 4.2.5 on 2023-11-08 14:04

from django.db import migrations
import recepts.fields
import recepts.models


class Migration(migrations.Migration):

    dependencies = [
        ('recepts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resipes',
            name='preview',
            field=recepts.fields.WEBPField(blank=True, null=True, upload_to=recepts.models.image_folder),
        ),
        migrations.AlterField(
            model_name='steps',
            name='photo',
            field=recepts.fields.WEBPField(upload_to=recepts.models.image_folder, verbose_name='Фото'),
        ),
    ]
