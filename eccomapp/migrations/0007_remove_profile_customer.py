# Generated by Django 4.1.1 on 2022-10-13 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eccomapp', '0006_profile_user_alter_profile_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='customer',
        ),
    ]
