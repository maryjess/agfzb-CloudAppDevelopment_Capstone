import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "../djangobackend/settings")

import django
django.setup()

from django.contrib import admin
from .models import CarModel, CarMake
# from .models import related models


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name',)

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ('name',)

# Register models here
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)
