
from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone

from clientes.models import Cliente
from habitaciones.models import Habitacion
from reservaciones.models import Reservacion


def dashboard(request):
    total_clientes = Cliente.objects.count()
    total_habitaciones = Habitacion.objects.count()
    total_reservaciones = Reservacion.objects.count()

    ocupadas = Reservacion.objects.filter(
        estado=Reservacion.ACTIVA,
        fecha_entrada__lte=timezone.localdate(),
        fecha_salida__gt=timezone.localdate()
    ).values_list('habitacion_id', flat=True).distinct()

    habitaciones_disponibles = Habitacion.objects.filter(
        disponible=True
    ).exclude(id__in=ocupadas).count()

    ingresos = Reservacion.objects.filter(
        estado__in=[Reservacion.ACTIVA, Reservacion.FINALIZADA]
    ).aggregate(total=Sum('total'))['total'] or 0

    contexto = {
        'total_clientes': total_clientes,
        'total_habitaciones': total_habitaciones,
        'total_reservaciones': total_reservaciones,
        'habitaciones_disponibles': habitaciones_disponibles,
        'ingresos': ingresos,
    }

    return render(request, 'dashboard.html', contexto)
