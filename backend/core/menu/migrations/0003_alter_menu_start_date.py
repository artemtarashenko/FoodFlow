# Generated by Django 4.2.5 on 2023-12-23 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_menu_alter_menuconfig_options_alter_menuconfig_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='start_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
