# Generated by Django 5.1.1 on 2024-10-25 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_billing_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billing_details',
            name='Mobile',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
