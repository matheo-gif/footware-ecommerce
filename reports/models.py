from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.EmailField(null=True, blank=True)
    image = models.ImageField(upload_to='admins')
    mobile_number = models.PositiveIntegerField(default=0)
