# Generated by Django 4.1.1 on 2022-10-14 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eccomapp', '0009_remove_order_product_remove_order_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='discount',
        ),
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.CharField(choices=[('White', 'White'), ('Black', 'Black'), ('Red', 'Red'), ('Pink', 'Pink'), ('yellow', 'yellow'), ('Yellow-black', 'Yellow-black'), ('Black-white', 'Black-white'), ('Blue-white', 'Blue-white'), ('Blue', 'Blue')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='discount',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='shoe_size',
            field=models.CharField(choices=[('White', 'White'), ('Black', 'Black'), ('Red', 'Red'), ('Pink', 'Pink')], max_length=50, null=True),
        ),
    ]
