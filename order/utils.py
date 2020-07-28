from django.db.models import Sum

from app.utils import get_session_key
from . import models


def get_products_in_cart(request):
    session_key = get_session_key(request)
    products_in_cart = models.ProductInCart.objects.filter(session_key=session_key).order_by('id')
    return products_in_cart or None


def clean_cart(request):
    session_key = get_session_key(request)
    products_in_cart = models.ProductInCart.objects.filter(session_key=session_key).order_by('id')
    for product in products_in_cart:
        product.delete()
    return True


def get_total_products_in_cart(request):
    products = get_products_in_cart(request)
    if not products:
        return None

    total_in_cart = products.aggregate(Sum('count'))['count__sum']
    return total_in_cart


def get_total_price_in_cart(request):
    products = get_products_in_cart(request)
    total_price_in_cart = 0

    if products:
        for product in products:
            total_price_in_cart += int(product.price) * int(product.count)
            if product.install:
                total_price_in_cart += int(product.install_price) * int(product.count)

    return int(total_price_in_cart)
