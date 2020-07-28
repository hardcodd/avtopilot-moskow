from app.forms import TextUs, CallBack
from app.utils import get_session_key
from catalog.models import Make
from navigation.models import Menu
from order.utils import get_products_in_cart, get_total_price_in_cart, get_total_products_in_cart
from settings.models import General


def cart_info(request):
    session_key = get_session_key(request)
    if not session_key:
        request.session.cycle_key()

    products_in_cart = get_products_in_cart(request)
    total_in_cart = get_total_products_in_cart(request)
    total_price_in_cart = get_total_price_in_cart(request)

    return locals()


def options(request):
    try:
        opts = General.objects.get(id=1)
    except General.DoesNotExist:
        opts = None
    return locals()


def makes_404(request):
    make_items_404 = Make.objects.all().order_by('title')
    return locals()


def menu(request):
    main_menu = Menu.objects.filter(slug='menu').first()
    footer_menu_1 = Menu.objects.filter(slug='footer-1').first()
    footer_menu_2 = Menu.objects.filter(slug='footer-2').first()
    footer_menu_3 = Menu.objects.filter(slug='footer-3').first()
    return locals()


def forms(request):
    text_us_form = TextUs(request.POST or None, initial={
        'to': 'Сообщение (Кнопка "Напишите" в шапке)'
    })

    callback_form = CallBack(request.POST or None, initial={
        'to': 'Заказ звонка (Кнопка "Перезвоним" в шапке)'
    })

    return locals()
