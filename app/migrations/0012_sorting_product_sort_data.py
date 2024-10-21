# Generated by Django 5.1.1 on 2024-10-03 08:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_price_product_price_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sorting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='sort_data',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.sorting'),
        ),
    ]