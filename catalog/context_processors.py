from catalog.models import Case, UniversalProduct


def widget_catalog(request):
    widget_cases = Case.objects.filter(status='PUBLIC').order_by('?')[:2]
    widget_accessories = UniversalProduct.objects.filter(status='PUBLISHED', product_type='ACCESSORY').order_by('?')[:2]
    return locals()
