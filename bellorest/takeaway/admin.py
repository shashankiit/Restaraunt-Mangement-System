from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Menu_item)
admin.site.register(Inventory)
admin.site.register(Ingredient_list)
admin.site.register(Order_Ingredient)