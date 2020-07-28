from django.core.paginator import Paginator


def pagination(request, objects, per_page=6):
    paginator = Paginator(objects, per_page)
    page = request.GET.get('page')
    objects = paginator.get_page(page)
    return objects


def check_page(request, objects):
    page = request.GET.get('page')
    if page and not objects.has_other_pages():
        return request.path
    elif page and not page.isdigit():
        return request.path
    elif page and page.isdigit() and int(page) <= 1:
        return request.path
    elif page and page.isdigit() and int(page) > objects.paginator.num_pages:
        return '%s?page=%s' % (request.path, objects.paginator.num_pages)
    return False
