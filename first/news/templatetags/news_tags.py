from django import template
from news.models import Category
from django.db.models import *


register = template.Library()

@register.inclusion_tag('news/list_categories.html')
def show_categories():
    categories= Category.objects.annotate(cnt=Count('news'),filter=F('news__is_publishied')).filter(cnt__gt=0)
    return {'categories':categories}



