from django import template

register = template.Library()


@register.filter(name="uploader_id")
def uploader_id(value):
    return value - 1
