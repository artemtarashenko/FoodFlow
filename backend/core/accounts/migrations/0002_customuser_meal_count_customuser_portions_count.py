# Generated by Django 4.2.5 on 2023-11-09 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='meal_count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='portions_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]