from django import template
from ..models import Category

register = template.Library()


@register.inclusion_tag('category/categories_nav.html')
def show_categories():
    categories = Category.objects.all().order_by('-name')
    return {'categories': categories}


@register.simple_tag
def breadcrumb_schema():
    return "http://schema.org/BreadcrumbList"


@register.inclusion_tag('breadcrumbs/breadcrumb_home.html')
def breadcrumb_home(url='/', title=''):
    return {
        'url': url,
        'title': title
    }


@register.inclusion_tag('breadcrumbs/breadcrumb_item.html')
def breadcrumb_item(url, title, position):
    return {
        'url': url,
        'title': title,
        'position': position
    }


@register.inclusion_tag('breadcrumbs/breadcrumb_active.html')
def breadcrumb_active(url, title, position):
    return {
        'url': url,
        'title': title,
        'position': position
    }
