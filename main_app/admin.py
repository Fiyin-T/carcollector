from django.contrib import admin

from . models import Car, Tuning, Photo

# Register your models here.
admin.site.register(Car)
admin.site.register(Tuning)
admin.site.register(Photo)