# Generated by Django 5.1.1 on 2024-10-10 07:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_additional_remove_product_sort_data_delete_sorting'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Additional_filter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.additional'),
        ),
    ]
