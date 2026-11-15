from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone

from clientes.models import Cliente
from habitaciones.models import Habitacion
from reservaciones.models import Reservacion


@login_required
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


@login_required
def reportes(request):
    # Los ingresos no cuentan las reservaciones canceladas
    validas = Reservacion.objects.exclude(estado=Reservacion.CANCELADA)

    ingresos_por_mes = (
        validas
        .annotate(mes=TruncMonth('fecha_entrada'))
        .values('mes')
        .annotate(reservaciones=Count('id'), ingresos=Sum('total'))
        .order_by('-mes')
    )

    nombres_tipo = dict(Habitacion.TIPOS)
    por_tipo = [
        {
            'tipo': nombres_tipo.get(fila['habitacion__tipo'], fila['habitacion__tipo']),
            'reservaciones': fila['reservaciones'],
            'ingresos': fila['ingresos'],
        }
        for fila in (
            validas
            .values('habitacion__tipo')
            .annotate(reservaciones=Count('id'), ingresos=Sum('total'))
            .order_by('-reservaciones')
        )
    ]

    mas_reservadas = (
        Habitacion.objects
        .annotate(total=Count(
            'reservaciones',
            filter=~Q(reservaciones__estado=Reservacion.CANCELADA)
        ))
        .filter(total__gt=0)
        .order_by('-total')[:5]
    )

    nombres_estado = dict(Reservacion.ESTADOS)
    por_estado = [
        {
            'estado': nombres_estado.get(fila['estado'], fila['estado']),
            'cantidad': fila['cantidad'],
        }
        for fila in (
            Reservacion.objects
            .values('estado')
            .annotate(cantidad=Count('id'))
            .order_by('-cantidad')
        )
    ]

    return render(request, 'reportes.html', {
        'ingresos_por_mes': ingresos_por_mes,
        'por_tipo': por_tipo,
        'mas_reservadas': mas_reservadas,
        'por_estado': por_estado,
    })