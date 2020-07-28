import json
import uuid

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Sum
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse, Http404
from yandex_money.forms import PaymentForm
from yandex_money.models import Payment

from app.utils import get_session_key, build_url, normalize_phone
from order.mail import order_mail, send_email_order_sew
from order.models import Order
from .utils import get_total_price_in_cart, get_products_in_cart, clean_cart

from . import models

import simplejson


BANNED_PAYMENT_TYPES = (
    'GP',
    'WM',
    'SB',
    'AB',
    'MA',
    'PB',
    'QW',
    'CR',
    'MC'
)


def products_in_cart(request):
    data = dict()
    session_key = get_session_key(request)

    data['total_in_cart'] = \
        models.ProductInCart.objects.filter(session_key=session_key).aggregate(Sum('count'))['count__sum'] or 0
    data['total_price_in_cart'] = get_total_price_in_cart(request)
    data['products_in_cart'] = list()

    products = get_products_in_cart(request)
    if products:
        for product in products:
            product_dict = dict()

            product_dict['title'] = product.title
            product_dict['id'] = product.pk
            product_dict['url'] = product.url
            product_dict['image'] = product.image
            product_dict['code'] = product.code
            product_dict['price'] = product.price
            product_dict['install_price'] = product.install_price
            product_dict['install'] = product.install
            if product.weight > 0:
                product_dict['weight'] = product.weight
            product_dict['size'] = product.size
            product_dict['material'] = product.material
            product_dict['color'] = product.color
            product_dict['count'] = product.count

            data['products_in_cart'].append(product_dict)

    return JsonResponse(data)


def ajax_get_delivery_methods(request):
    data = dict()
    try:
        data['delivery_methods'] = serializers.serialize('json', models.DeliveryMethod.objects.all().order_by('order'))
    except:
        pass

    return JsonResponse(data)


def add_to_cart(request):
    session_key = get_session_key(request)
    add_data = request.POST

    id_to_plus = add_data.get('id')
    product_count = add_data.get('product_count')
    if add_data.get('product_install') == 'True':
        install = True
    else:
        install = False

    if id_to_plus:
        if models.ProductInCart.objects.filter(session_key=session_key, id=id_to_plus).exists():
            product = models.ProductInCart.objects.get(session_key=session_key, id=id_to_plus)
            if product:
                if int(product_count) > 0:
                    product.count = product_count
                    product.install = install
                    product.save(force_update=True)
                else:
                    product.delete()

    else:
        new_product, created = models.ProductInCart.objects.get_or_create(
            session_key=session_key,
            title=add_data.get('product_title'),
            product_id=add_data.get('product_id'),
            url=add_data.get('product_url'),
            image=add_data.get('product_image'),
            code=add_data.get('product_code'),
            price=add_data.get('product_price'),
            weight=add_data.get('product_weight'),
            install_price=add_data.get('product_install_price'),
            size=add_data.get('product_size'),
            material=add_data.get('product_material'),
            color=add_data.get('product_color'),
            install=install,
            defaults={'count': add_data.get('product_count')}
        )
        if not created:
            new_product.count += int(add_data.get('product_count'))
            new_product.save(force_update=True)

    return products_in_cart(request)


def remove_from_cart(request):
    session_key = get_session_key(request)
    product_id = request.POST.get('id')

    product = models.ProductInCart.objects.get(session_key=session_key, id=product_id)
    if product:
        product.delete()

    return products_in_cart(request)


def order(request):
    if request.method == 'POST':
        products = get_products_in_cart(request)
        data = request.POST
        products_info = ''
        total_price = get_total_price_in_cart(request)
        default_price = data.get('default_price')
        promo = data.get('promo')
        promo_price = data.get('promo_price')
        promo_code = data.get('promo_code')

        if not products:
            return JsonResponse({'success': False})

        products_json = serializers.serialize('json', products)

        open_tr_td = '<tr><td style="padding:10px;border:1px solid #e9e9e9">'
        meddle_td_td = '</td><td style="padding:10px;border:1px solid #e9e9e9">'

        for num, product in enumerate(products):
            products_info += f'<thead style="background:#445;color:#fff;text-align:left">' \
                             f'<tr><th colspan="2" style="padding:10px">' \
                             f'{str(product.title)}</th>'
            products_info += f'<tbody>{open_tr_td}ID товара{meddle_td_td}{str(product.product_id)}</td></tr>'
            if product.material:
                products_info += f'{open_tr_td}Материал{meddle_td_td}{str(product.material)}</td></tr>'
            if product.color:
                products_info += f'{open_tr_td}Цвет{meddle_td_td}{str(product.color)}</td></tr>'
            if product.code:
                products_info += f'{open_tr_td}Артикул{meddle_td_td}{str(product.code)}</td></tr>'
            if product.size:
                products_info += f'{open_tr_td}Размер{meddle_td_td}{str(product.size)}</td></tr>'
            products_info += f'{open_tr_td}Цена за штуку{meddle_td_td}{str(product.price)}</td></tr>'
            if product.install:
                products_info += f'{open_tr_td}Установка{meddle_td_td}Да (+{str(product.install_price)})</td></tr>'
            else:
                products_info += f'{open_tr_td}Установка{meddle_td_td}Нет</td></tr>'
            products_info += f'{open_tr_td}Количество{meddle_td_td}{str(product.count)}</td></tr>'
            if not num + 1 == products.count():
                products_info += '<tbody>'

        products_info += '<thead style="background:#445;color:#fff">' \
                         '<tr><td colspan="2" style="padding:10px">ИТОГ</td><tr></thead>' \
                         '<tfoot>'

        if default_price and promo_price:
            products_info += f'{open_tr_td}Промокод{meddle_td_td}{promo_code}</td></tr>'
            products_info += f'{open_tr_td}Скидка по промокоду{meddle_td_td}{promo}%</td></tr>'
            products_info += f'{open_tr_td}Итоговая сумма по промокоду{meddle_td_td}{promo_price}</td></tr>'
            products_info += f'{open_tr_td}Итоговая сумма без промокода{meddle_td_td}{default_price}</td></tr>'
        else:
            products_info += f'{open_tr_td}Итоговая сумма{meddle_td_td}{total_price}</td></tr>'

        if data.get('comment'):
            products_info += f'{open_tr_td}Комментарий{meddle_td_td}{data.get("comment")}</td></tr>'

        products_info += '</tfoot>'
        products_info = f'<table style="width:100%">{products_info}</table>'

        user_id = None
        if request.user.is_authenticated:
            user_id = request.user.id

        try:
            delivery_method = models.DeliveryMethod.objects.get(title=data.get('delivery_method'))
        except ObjectDoesNotExist:
            delivery_method = None

        new_order = Order.objects.create(
            user_id=user_id,
            email=data.get('email'),
            full_name=data.get('full_name'),
            phone=data.get('phone'),
            address=data.get('delivery_address'),
            delivery=delivery_method,
            pay_method=data.get('pay_method'),
            price=promo_price or total_price,
            amount=len(products),
            products_info=products_info,
            products_json=products_json,
        )

        clean_cart(request)
        order_mail(request, new_order)

        return JsonResponse({'success': True})
    return HttpResponseNotFound()


def order_sew(request):
    if request.method == 'POST':
        data = request.POST

        info = ''
        total_price = 0
        contacts = None
        for key in data:
            if key != 'Общая сумма' and key != 'contacts':
                info += '%s: %s<br>' % (key, data[key])
            elif key == 'Общая сумма':
                total_price = data[key]
            elif key == 'contacts':
                contacts = json.loads(data[key])

        message = f'{info}<br>Общая сумма: <b>{total_price}</b>руб.<hr><b>Дополнительная информация</b>:<br>'

        for key in contacts:
            message += f'{key}: {contacts[key]}<br>'

        send_email_order_sew(request, message)

        return JsonResponse({'success': True})
    return HttpResponseNotFound()


def yandex_payment(request, pk, _uuid):
    _order = get_object_or_404(Order, pk=pk)
    if _order.payment_status != Order.PAYMENT_AVAILABLE or str(_order.uuid) != str(_uuid):
        raise Http404("Payment not available")

    order_sum = float(_order.price)

    if _order.delivery and _order.delivery.price:
        order_sum += float(_order.delivery.price)

    try:
        email = _order.email
        phone = normalize_phone(_order.phone)
        payment = _order.payment

        if not payment:
            payment_params = {
                'order_amount': order_sum,
                'order_number': _order.pk,
                'cps_email': email,
                'cps_phone': phone
            }
            try:
                payment = Payment(**payment_params)
                payment.save()
            except Exception as e:
                payment = Payment.objects.filter(order_number=_order.pk).first()
                if not payment:
                    raise e
            _order.payment = payment
            _order.save()

        receipt_items = []
        items = json.loads(_order.products_json)

        for item in items:
            obj = {
                'text': item['fields']['title'],
                'quantity': item['fields']['count'],
                'tax': 1,
                'price': {
                    'amount': float(item['fields']['price'])
                }
            }
            if item['fields']['install']:
                obj['price']['amount'] += float(item['fields']['install_price'])
            receipt_items.append(obj)

        delivery = _order.delivery
        if delivery and delivery.price:
            receipt_items.append({
                'text': u'Доставка',
                'quantity': 1,
                'tax': 1,
                'price': {
                    "amount": float(delivery.price)
                }
            })

        customer_contact = email or phone
        receipt = {
            'customerContact': customer_contact,
            'items': receipt_items
        }

        payment_form = PaymentForm(instance=payment)
        type_choices = payment_form.fields['paymentType'].widget.choices
        payment_form.fields['paymentType'].widget.choices = \
            [choice for choice in type_choices if choice[0] not in BANNED_PAYMENT_TYPES]

        context = {
            'form': payment_form,
            'receipt': simplejson.dumps(receipt),
            'customer_contact': customer_contact
        }

        return render(request, 'yandex_money_form.html', context)
    except Exception as e:
        raise Http404("Unknown problem: %s" % str(e))
