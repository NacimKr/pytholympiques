# Generated by Django 5.0.7 on 2024-08-22 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.RemoveField(
            model_name='product',
            name='is_commanded',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
