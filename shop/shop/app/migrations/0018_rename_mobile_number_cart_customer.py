# Generated by Django 5.0.6 on 2024-07-15 06:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_remove_cart_customer_cart_mobile_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='mobile_number',
            new_name='customer',
        ),
    ]
