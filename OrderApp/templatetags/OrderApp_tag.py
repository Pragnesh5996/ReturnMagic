from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.simple_tag
def setvar(val=None):
  return val

@register.filter
def get_at_index(list, index):
  if len(list) > index:
      gotdata = list[index]
  else: 
      gotdata = 0

  return gotdata