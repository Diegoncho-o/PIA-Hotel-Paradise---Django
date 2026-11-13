from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellidos', 'correo', 'telefono', 'fecha_registro')
    search_fields = ('nombre', 'apellidos', 'correo', 'telefono')
    readonly_fields = ('fecha_registro',)

    
# Register your models here.
