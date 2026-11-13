from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, ProtectedError

from .models import Cliente
from .forms import ClienteForm


def lista_clientes(request):
    clientes = Cliente.objects.all()

    # Buscador de clientes por nombre o correo
    q = request.GET.get('q', '').strip()
    if q:
        clientes = clientes.filter(Q(nombre__icontains=q) | Q(correo__icontains=q))

    contexto = {
        'clientes': clientes,
        'q': q,
    }
    # Corregido a minúsculas 'clientes/lista.html' para que coincida con tu carpeta
    return render(request, 'clientes/lista.html', contexto)


def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente creado correctamente.')
           
            return redirect('clientes:lista')
    else:
        form = ClienteForm()

    return render(request, 'clientes/form.html', {
        'form': form,
        'titulo': 'Nuevo cliente'
    })


def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado correctamente.')
            return redirect('clientes:lista')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'clientes/form.html', {
        'form': form,
        'titulo': f'Editar cliente {cliente.nombre}'
    })


def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        try:
            cliente.delete()
            messages.success(request, 'Cliente eliminado correctamente.')
        except ProtectedError:
            messages.error(
                request,
                'No se puede eliminar el cliente porque tiene reservaciones asociadas.'
            )
        return redirect('clientes:lista')

    return render(request, 'clientes/confirmar_eliminar.html', {
        'cliente': cliente
    })
# Create your views here.
