from django.shortcuts import render, redirect, get_object_or_404
from ..models import Laptop  # Correcto: sale de 'views' para buscar el modelo
from django.db.models import Sum, F


def admi_product(request):
    """Gestión integral del inventario MasterLaps"""

    # 1. Lógica para GUARDAR (POST)
    if request.method == 'POST':
        modelo = request.POST.get('modelo')
        marca = request.POST.get('marca')
        estado = request.POST.get('estado')
        costo = request.POST.get('costo')
        precio_venta = request.POST.get('precio_venta')
        procesador = request.POST.get('procesador')
        ram_gb = request.POST.get('ram_gb')
        almacenamiento = request.POST.get('almacenamiento')
        stock = request.POST.get('stock')
        imagen = request.FILES.get('imagen')  # Importante para las fotos

        # Creamos el registro en la base de datos
        Laptop.objects.create(
            modelo=modelo,
            marca=marca,
            estado=estado,
            costo=costo,
            precio_venta=precio_venta,
            procesador=procesador,
            ram_gb=ram_gb,
            almacenamiento=almacenamiento,
            stock=stock,
            imagen=imagen
        )
        return redirect('admi_product')

    # 2. Lógica para MOSTRAR (GET)
    laptops = Laptop.objects.all().order_by('-id')

    # Cálculos para los cuadros de arriba
    inversion = laptops.aggregate(total=Sum(F('costo') * F('stock')))['total'] or 0
    ganancia_total = laptops.aggregate(
        total=Sum((F('precio_venta') - F('costo')) * F('stock'))
    )['total'] or 0

    # Resumen por marcas
    stock_marcas = Laptop.objects.values('marca').annotate(total=Sum('stock'))

    context = {
        'laptops': laptops,
        'inversion': inversion,
        'ganancia_total': ganancia_total,
        'stock_marcas': stock_marcas,
    }
    return render(request, 'products/admi_product.html', context)


# --- Agrega estas para que no den error en urls.py ---

def editar_laptop(request, pk):
    laptop = get_object_or_404(Laptop, pk=pk)
    # Aquí irá la lógica de edición más adelante
    return redirect('admi_product')


def eliminar_laptop(request, pk):
    laptop = get_object_or_404(Laptop, pk=pk)
    laptop.delete()
    return redirect('admi_product')