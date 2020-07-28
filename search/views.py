from django.contrib.postgres.search import SearchVector
from django.http import HttpResponseNotFound
from django.shortcuts import render

from catalog.models import Case, UniversalProduct


def search(request):
    if request.method == 'POST':
        search_string = request.POST.get('q')

        cases = Case.objects.annotate(
            search=SearchVector('title', 'description', 'meta_description', 'meta_keywords')
        ).filter(search=search_string, status='PUBLIC')

        products = UniversalProduct.objects.annotate(
            search=SearchVector('title', 'description', 'meta_description', 'meta_keywords')
        ).filter(search=search_string, status='PUBLIC')

        instance = {
            'title': 'Поиск: %s' % search_string
        }
        context = {
            'instance': instance,
            'search_string': search_string,
            'cases': cases,
            'products': products,
            'posts': posts
        }
        return render(request, 'search/search.html', context)
    return HttpResponseNotFound()
