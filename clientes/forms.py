from django import forms
from .models import Cliente
import re
class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ['nombre', 'apellidos', 'correo', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'correo': {
                'unique': 'Ya existe un cliente registrado con este correo.',
                'invalid': 'Escribe un correo válido, por ejemplo nombre@dominio.com.',
            },
        }

    def clean_correo(self):
        return self.cleaned_data['correo'].strip().lower()

    def clean_nombre(self):
        return self.cleaned_data['nombre'].strip().title()

    def clean_apellidos(self):
        return self.cleaned_data['apellidos'].strip().title()

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        # Quitar espacios, guiones y paréntesis
        limpio = re.sub(r'[\s\-\(\)]', '', telefono)
        if not re.fullmatch(r'\+?\d{10,15}', limpio):
            raise forms.ValidationError(
                'Escribe un teléfono válido de 10 a 15 dígitos (puede iniciar con +).'
            )
        return limpio