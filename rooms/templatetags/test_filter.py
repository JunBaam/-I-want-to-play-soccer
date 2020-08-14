from django import template

register = template.Library()


@register.filter
def filtertt(value):
    print(value)
    return "이것이 필터로군"
