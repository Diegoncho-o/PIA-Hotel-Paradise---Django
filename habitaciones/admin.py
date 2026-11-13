from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Habitacion



@admin.register(Habitacion)
class HabitacionAdmin(admin.ModelAdmin):
    list_display = ('numero', 'tipo', 'precioxnoche', 'capacidad', 'disponible')
    list_filter = ('tipo', 'disponible')
    search_fields = ('numero',)
    list_editable = ('disponible',)

