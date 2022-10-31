# Generated by Django 4.1.1 on 2022-10-13 09:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eccomapp', '0002_order_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(max_length=300, null=True)),
                ('image', models.ImageField(default='images/user.jpg', upload_to='profileimg')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eccomapp.customer')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
