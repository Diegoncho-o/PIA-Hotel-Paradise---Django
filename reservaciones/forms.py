from django import forms

from habitaciones.models import Habitacion
from .models import Reservacion


class ReservacionForm(forms.ModelForm):

    class Meta:
        model = Reservacion
        fields = ['cliente', 'habitacion', 'fecha_entrada', 'fecha_salida']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'habitacion': forms.Select(attrs={'class': 'form-select'}),
            'fecha_entrada': forms.DateInput(
                format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_salida': forms.DateInput(
                format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
        }


class DisponibilidadForm(forms.Form):
    fecha_entrada = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', 'class': 'form-control'}))
    fecha_salida = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', 'class': 'form-control'}))
    tipo = forms.ChoiceField(
        choices=[('', 'Todos los tipos')] + Habitacion.TIPOS,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    def clean(self):
        datos = super().clean()
        entrada = datos.get('fecha_entrada')
        salida = datos.get('fecha_salida')
        if entrada and salida and salida <= entrada:
            raise forms.ValidationError(
                'La fecha de salida debe ser mayor que la fecha de entrada.')
        return datos