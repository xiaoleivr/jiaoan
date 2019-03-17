from django import template
from ..models import Category

register = template.Library()

@register.inclusion_tag('post/category.html')
def show_categorys():
    categories = Category.objects.all()
    return {'categories':categories}