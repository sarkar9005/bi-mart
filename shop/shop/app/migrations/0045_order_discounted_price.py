# Generated by Django 5.0.6 on 2024-07-22 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0044_order_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='discounted_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
