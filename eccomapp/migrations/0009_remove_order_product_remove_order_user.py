# Generated by Django 4.1.1 on 2022-10-13 18:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eccomapp', '0008_order_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
    ]