# Generated by Django 4.1 on 2024-06-16 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_category_heading'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='img',
            field=models.ImageField(null=True, upload_to='category'),
        ),
    ]
