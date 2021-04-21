from django import template
from ..models import Category

register = template.Library()


@register.inclusion_tag('category/categories_nav.html')
def show_categories():
    categories = Category.objects.all().order_by('-name')
    return {'categories': categories}
