# Generated by Django 4.2.5 on 2023-12-20 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recepts', '0006_dimensions_remove_resipesingredients_dimension'),
    ]

    operations = [
        migrations.AddField(
            model_name='resipesingredients',
            name='dimension',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='recepts.dimensions'),
        ),
    ]