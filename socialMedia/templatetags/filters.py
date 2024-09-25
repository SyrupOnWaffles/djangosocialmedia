from django import template

register = template.Library()
@register.filter(name="dasame")
def dasame(things, category):
    return things.filter(created_by=category).exists()