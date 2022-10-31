from django.contrib import admin
from .models import *

admin.site.site_header = "Toplook Footware"
admin.site.index_title = "Toplook Footware "


admin.site.register([Customer, Category, Product,
                    CartProduct, Cart, Order, Profile, Contact])

# Register your models here.
