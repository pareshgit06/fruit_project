# Generated by Django 5.1.1 on 2024-10-02 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_rename_cat_id_product_cat_id_1'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='cat_id_1',
            new_name='cat_id',
        ),
    ]
