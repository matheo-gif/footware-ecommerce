# Generated by Django 4.1.1 on 2022-10-13 09:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eccomapp', '0003_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.AlterField(
            model_name='profile',
            name='customer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='eccomapp.customer'),
        ),
    ]
