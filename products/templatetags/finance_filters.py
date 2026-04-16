from django import template

register = template.library()

@register.filter
def subtract(value, arg):
    """Resta el argumento del valor (precio_venta - costo)"""
    try:
        return value - arg
    except (TypeError, ValueError):
        return 0