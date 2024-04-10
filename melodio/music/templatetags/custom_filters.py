from django import template

register = template.Library()

@register.filter
def duration_format(duration):
    minutes = duration // 60
    seconds = duration % 60
    return f"{minutes}:{seconds:02d}"
