
from django import forms
from .models import Habitacion


class HabitacionForm(forms.ModelForm):

    class Meta:
        model = Habitacion
        fields = ['numero', 'tipo', 'precioxnoche', 'capacidad', 'disponible', 'imagen']

        labels = {
            'numero': 'Número de habitación',
            'precioxnoche': 'Precio por noche',
        }

        widgets = {
            'numero': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'precioxnoche': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

    def clean_precioxnoche(self):
        precio = self.cleaned_data['precioxnoche']
        if precio <= 0:
            raise forms.ValidationError('El precio por noche debe ser mayor que 0.')
        return precio

    def clean_capacidad(self):
        capacidad = self.cleaned_data['capacidad']
        if capacidad < 1:
            raise forms.ValidationError('La capacidad debe ser de al menos 1 persona.')
        return capacidad

    def clean_numero(self):
        numero = self.cleaned_data['numero']

        if numero <= 0:
            raise forms.ValidationError('El número de habitación debe ser positivo.')

        habitaciones = Habitacion.objects.filter(numero=numero)

        if self.instance.pk:
            habitaciones = habitaciones.exclude(pk=self.instance.pk)

        if habitaciones.exists():
            raise forms.ValidationError('Ya existe una habitación con ese número.')

        return numero





