from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from habitaciones.models import Habitacion
from .forms import ReservacionForm, DisponibilidadForm
from .models import Reservacion


def lista_reservaciones(request):
    reservaciones = Reservacion.objects.select_related('cliente', 'habitacion')

    q = request.GET.get('q', '').strip()
    tipo = request.GET.get('tipo', '')
    estado = request.GET.get('estado', '')

    if q:
        condicion = (Q(cliente__nombre__icontains=q) |
                     Q(cliente__apellidos__icontains=q))
        if q.isdigit():
            condicion |= Q(habitacion__numero=q)
        reservaciones = reservaciones.filter(condicion)
    if tipo:
        reservaciones = reservaciones.filter(habitacion__tipo=tipo)
    if estado:
        reservaciones = reservaciones.filter(estado=estado)

    return render(request, 'reservaciones/lista.html', {
        'reservaciones': reservaciones,
        'tipos': Habitacion.TIPOS,
        'estados': Reservacion.ESTADOS,
        'q': q, 'tipo_actual': tipo, 'estado_actual': estado,
    })


def consultar_disponibilidad(request):
    form = DisponibilidadForm(request.GET or None)
    libres = None

    if form.is_valid():
        entrada = form.cleaned_data['fecha_entrada']
        salida = form.cleaned_data['fecha_salida']
        tipo = form.cleaned_data['tipo']

        ocupadas = Reservacion.objects.filter(
            estado=Reservacion.ACTIVA,
            fecha_entrada__lt=salida,
            fecha_salida__gt=entrada,
        ).values_list('habitacion_id', flat=True)

        libres = Habitacion.objects.filter(disponible=True).exclude(id__in=ocupadas)
        if tipo:
            libres = libres.filter(tipo=tipo)

    return render(request, 'reservaciones/disponibilidad.html',
                  {'form': form, 'libres': libres})



def crear_reservacion(request):
    if request.method == 'POST':
        form = ReservacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reservación creada correctamente.')
            return redirect('reservaciones:lista')
    else:
        form = ReservacionForm()

    return render(request, 'reservaciones/form.html', {
        'form': form,
        'titulo': 'Nueva reservación',
    })


def editar_reservacion(request, pk):
    reservacion = get_object_or_404(Reservacion, pk=pk)

    if reservacion.estado != Reservacion.ACTIVA:
        messages.error(request, 'Solo se pueden editar reservaciones activas.')
        return redirect('reservaciones:lista')

    if request.method == 'POST':
        form = ReservacionForm(request.POST, instance=reservacion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reservación actualizada correctamente.')
            return redirect('reservaciones:lista')
    else:
        form = ReservacionForm(instance=reservacion)

    return render(request, 'reservaciones/form.html', {
        'form': form,
        'titulo': f'Editar reservación #{reservacion.pk}',
    })


def cancelar_reservacion(request, pk):
    reservacion = get_object_or_404(Reservacion, pk=pk)

    if request.method == 'POST':
        if reservacion.estado != Reservacion.ACTIVA:
            messages.error(request, 'Esta reservación ya no está activa.')
        else:
            reservacion.estado = Reservacion.CANCELADA
            reservacion.save(update_fields=['estado'])
            messages.success(request, 'Reservación cancelada correctamente.')
        return redirect('reservaciones:lista')

    return render(request, 'reservaciones/confirmar_cancelar.html', {
        'reservacion': reservacion,
    })
# Create your views here.
