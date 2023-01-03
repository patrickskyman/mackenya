from categories.models import Category 
from mackenya import settings

def utills(request): 
    return {
            'categories': Category(request),
            'categories': Category.objects.all(),
            'site_name': settings.SITE_NAME,
            'meta_keywords': settings.META_KEYWORDS,
            'meta_description': settings.META_DESCRIPTION,
            'request': request }