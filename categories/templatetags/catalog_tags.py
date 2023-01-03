from django import template
from categories.models import Product

register = template.Library()

@register.inclusion_tag("tags/product_list.html") 

def product_list(products, header_text):
    return { 'products': products,
            'header_text': header_text }