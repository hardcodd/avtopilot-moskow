from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def order_mail(request, order):
    user = order.full_name
    order_info = ''
    order_info += '<p><b>Способ доставки:</b> %s</p>' % order.delivery
    if order.address:
        order_info += '<p><b>Адрес доставки:</b> %s</p>' % order.address
    order_info += '<p><b>Предварительная сумма заказа:</b> %s руб.</p>' % order.price
    order_info += '<br><b>Информация о товарах:</b><br><br>'
    order_info += order.products_info

    subject = f'AVTOPILOT: Ваш заказ #{order.id} успешно оформлен. «{request.build_absolute_uri(location="/")}»'

    html_message = '<h3>Здравствуйте, %s!</h3>' \
                   '<p>Ваш заказ №%s принят.</p>' \
                   '<p>Наш менеджер свяжется с Вами для уточнения деталей заказа в ближайшее время.</p>' \
                   '<div><h4>Информация о заказе:</h4>%s</div>'\
                   % (user, order.id, order_info)

    send_mail(
        subject=subject,
        message=html_message,
        html_message=html_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[order.email]
    )


def send_email_user_notification_order_changed(email_to, order, subject, template):
    """Отправка сообщения пользователю об изменениях в заказе"""

    message = render_to_string(template, {"order": order})
    try:
        send_mail(
            subject=subject,
            message=message,
            html_message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email_to],
            fail_silently=False
        )
    except:
        pass


def send_email_user_notification(email_to, _order):
    """Отправка сообщения пользователю об успешном оформлении заказа"""

    email_from = settings.DEFAULT_FROM_EMAIL
    message = render_to_string('messages/email_to_client_order_confirm.txt', {"order": _order})
    send_mail(u'Avtopilot_1: Ваш заказ успешно оформлен.', message, email_from, [email_to], fail_silently=False)


def send_email_order_sew(request, message):
    send_mail(
        subject=f'Новая заказ на пошив с сайта AVTOPILOT «{request.build_absolute_uri(location="/")}»',
        message=message,
        html_message=message,
        recipient_list=settings.RECIPIENT_LIST,
        from_email=settings.DEFAULT_FROM_EMAIL
    )
