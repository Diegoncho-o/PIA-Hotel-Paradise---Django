from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import ProtectedError

from .models import Habitacion
from .forms import HabitacionForm
def lista_habitaciones(request):
    habitaciones = Habitacion.objects.all()

    # Parámetros de búsqueda que vienen en la URL: ?q=101&tipo=suite
    q = request.GET.get('q', '').strip()
    tipo = request.GET.get('tipo', '')

    if q.isdigit():
        habitaciones = habitaciones.filter(numero=q)
    if tipo:
        habitaciones = habitaciones.filter(tipo=tipo)

    contexto = {
        'habitaciones': habitaciones,
        'tipos': Habitacion.TIPOS,
        'q': q,
        'tipo_actual': tipo,
    }
    return render(request, 'habitaciones/lista.html', contexto)

def crear_habitacion(request):
    if request.method == 'POST':
        form = HabitacionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Habitación creada correctamente.')
            return redirect('habitaciones:lista')
    else:
        form = HabitacionForm()

    return render(request, 'habitaciones/form.html',
                  {'form': form, 'titulo': 'Nueva habitación'})


def editar_habitacion(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk)

    if request.method == 'POST':
        form = HabitacionForm(request.POST, request.FILES, instance=habitacion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Habitación actualizada correctamente.')
            return redirect('habitaciones:lista')
    else:
        form = HabitacionForm(instance=habitacion)

    return render(request, 'habitaciones/form.html',
                  {'form': form, 'titulo': f'Editar habitación {habitacion.numero}'})


def eliminar_habitacion(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk)

    if request.method == 'POST':
        try:
            habitacion.delete()
            messages.success(request, 'Habitación eliminada correctamente.')
        except ProtectedError:
            messages.error(
                request,
                'No se puede eliminar la habitación porque tiene reservaciones asociadas.'
            )
        return redirect('habitaciones:lista')

    return render(request, 'habitaciones/confirmar_eliminar.html',
                  {'habitacion': habitacion})


# Create your views here.
