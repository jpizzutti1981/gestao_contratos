from django import template
from django.forms import BoundField
import os

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    if isinstance(field, BoundField):
        return field.as_widget(attrs={"class": css_class})
    # Se não for um campo de formulário, retorna o valor original
    return field

@register.filter
def basename(value):
    """Retorna apenas o nome do arquivo sem o path"""
    if not value:
        return ""
    return os.path.basename(str(value))
