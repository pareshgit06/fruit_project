# Generated by Django 5.1.1 on 2024-10-18 07:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_product_quantity_add_to_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Add_to_Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='media')),
                ('price', models.IntegerField()),
                ('product_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.product')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.user')),
            ],
        ),
    ]