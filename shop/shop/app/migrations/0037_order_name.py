# Generated by Django 5.0.6 on 2024-07-21 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0036_brand_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='name',
            field=models.CharField(default='', max_length=10),
        ),
    ]
