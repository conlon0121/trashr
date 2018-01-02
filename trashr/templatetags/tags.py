from django import template


register = template.Library()


@register.filter
def get_color(l, index):
    try:
        return l[index]
    except:
        return None