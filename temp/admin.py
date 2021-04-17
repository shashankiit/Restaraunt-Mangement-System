from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(loyalty_level)
admin.site.register(menu_items)