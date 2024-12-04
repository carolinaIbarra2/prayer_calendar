from django import template

register = template.Library()

@register.filter
def key_exists(dictionary, key):
    """Verifica si una clave existe en el diccionario."""
    return key in dictionary

@register.filter
def key_get(dictionary, key):
    """Obtiene el valor asociado a una clave en el diccionario."""
    return dictionary.get(key, "")

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, None)