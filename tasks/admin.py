from django.contrib import admin
from .models import Producto

class productoadmion(admin.ModelAdmin):
    readonly_fields = ("creacion", )

# Register your models here.
admin.site.register(Producto,productoadmion)
