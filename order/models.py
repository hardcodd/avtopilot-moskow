from django.db import models
from django.dispatch import receiver
from yandex_money.models import Payment
from yandex_money.signals import payment_completed

import uuid

from order.mail import send_email_user_notification


class ProductInCart(models.Model):
    session_key = models.CharField(max_length=256, verbose_name='Ключ сессии')
    product_id = models.PositiveIntegerField(verbose_name='ID товара')
    url = models.CharField(max_length=255, verbose_name='Ссылка')
    title = models.CharField(max_length=500, verbose_name='Заголовок')
    image = models.CharField(max_length=255, verbose_name='Изображение', blank=True, null=True)
    code = models.CharField(max_length=20, verbose_name='Код товара', blank=True, null=True)
    price = models.PositiveIntegerField(verbose_name='Цена за штуку')
    install = models.BooleanField(verbose_name='Установка', default=False)
    install_price = models.PositiveIntegerField(verbose_name='Цена за установку', blank=True, null=True)
    weight = models.FloatField(verbose_name='Вес товара (кг)', blank=True, null=True)
    size = models.CharField(max_length=128, verbose_name='Размер', blank=True, null=True)
    count = models.PositiveIntegerField(verbose_name='Количество')
    material = models.CharField(max_length=255, verbose_name='Материал', blank=True, null=True)
    color = models.CharField(max_length=255, verbose_name='Цвет', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары в корзине'


class DeliveryMethod(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=255)
    price = models.PositiveIntegerField(
        verbose_name='Стоимость доставки',
        help_text='Если установить значение "0", то доставка отобразится как бесплатная, <br>'
                  'Если поле оставить пустым, то заказчик увидит подпись "Уточняйте у менеджера"',
        blank=True, null=True
    )
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        verbose_name = 'Способ доставки'
        verbose_name_plural = 'Способы доставки'
        ordering = ['order']

    def __str__(self):
        return self.title


class Order(models.Model):

    STATUS_IN_PROGRESS = 1
    STATUS_DELIVERED = 2
    STATUS_REJECTED = 3
    STATUS_NOT_PHONE_CALL = 4
    STATUS_CONFIRMED = 5
    STATUS_SELF_DELIVERY = 6
    STATUS_INSTALLING = 7
    STATUS_DELIVERY = 8
    STATUS_COMPANY_DELIVERY = 9
    STATUS_POSTAL_DELIVERY = 10
    STATUS_ONLINE_PAYMENT_AVAILABLE = 11
    STATUS_PAID = 12
    STATUS_CHOICES = (
        (STATUS_IN_PROGRESS, u'Заказ принят'),
        (STATUS_CONFIRMED, u'Подтвержден'),
        (STATUS_SELF_DELIVERY, u'Самовывоз'),
        (STATUS_INSTALLING, u'Установка'),
        (STATUS_DELIVERY, u'Доставка'),
        (STATUS_COMPANY_DELIVERY, u'Отправка ТК'),
        (STATUS_POSTAL_DELIVERY, u'Отправка почтой'),
        (STATUS_ONLINE_PAYMENT_AVAILABLE, u'Доступен для оплаты онлайн'),
        (STATUS_PAID, u'Оплачен'),
        (STATUS_DELIVERED, u'Выполнен'),
        (STATUS_NOT_PHONE_CALL, u'Не дозвонились'),
        (STATUS_REJECTED, u'Отменен'),
    )

    PAYMENT_UNAVAILABLE = 1
    PAYMENT_AVAILABLE = 2
    PAYMENT_WAITING = 3
    PAYMENT_RECEIVED = 4
    PAYMENT_CHOICES = (
        (PAYMENT_UNAVAILABLE, u'Оплата недоступна'),
        (PAYMENT_AVAILABLE, u'Доступна оплата'),
        (PAYMENT_WAITING, u'Ожидается получение оплаты'),
        (PAYMENT_RECEIVED, u'Оплачен'),
    )

    uuid = models.CharField(max_length=256, verbose_name='UUID', default=uuid.uuid4())

    current_status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES,
                                                      default=STATUS_IN_PROGRESS,
                                                      verbose_name=u'текущий статус')
    payment_status = models.PositiveSmallIntegerField(choices=PAYMENT_CHOICES,
                                                      default=PAYMENT_UNAVAILABLE,
                                                      verbose_name=u'Статус оплаты')
    delivery = models.ForeignKey(DeliveryMethod, verbose_name='Способ доставки',
                                 blank=True,
                                 null=True,
                                 on_delete=models.CASCADE,
                                 related_name='delivery_method')
    amount = models.PositiveSmallIntegerField(verbose_name='Общее кол-во предметов', blank=True, null=True)
    pay_method = models.CharField(verbose_name='Способ оплаты', max_length=255, blank=True, null=True)
    price = models.CharField(verbose_name='Сумма покупки', max_length=255, blank=True, null=True)

    payment = models.ForeignKey(Payment, verbose_name='Платеж',
                                blank=True, null=True, on_delete=models.CASCADE)

    products_json = models.TextField(verbose_name='JSON Информация о товарах', blank=True, null=True)
    products_info = models.TextField(verbose_name='Информация о товарах')
    timestamp = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(verbose_name='Комментарий', blank=True, null=True)

    user_id = models.PositiveIntegerField(verbose_name='ID пользователя', blank=True, null=True)
    email = models.EmailField(max_length=255, verbose_name='E-mail', blank=True, null=True)
    full_name = models.CharField(verbose_name='Полное имя', max_length=255, blank=True, null=True)
    phone = models.CharField(verbose_name='Телефон', max_length=255, blank=True, null=True)
    address = models.CharField(verbose_name='Адрес доставки', max_length=255, blank=True, null=True)

    yandex_payment_req = models.CharField(u'yandex payment req id', blank=True, null=True, max_length=255)
    yandex_payment_id = models.CharField(u'yandex payment id', blank=True, null=True, max_length=255)

    __original_payment_status = None
    __original_current_status = None

    def __str__(self):
        return "Order #%d" % self.pk

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __init__(self, *args, **kwargs):
        super(Order, self).__init__(*args, **kwargs)
        self.was_delivery = self.delivery
        self.__original_payment_status = self.payment_status
        self.__original_current_status = self.current_status
        self.__original_amount = self.amount

    # При сохранении пересчитываем общую сумму. Т.к. может измениться способ доставки.
    def save(self, *args, **kwargs):

        if (self.was_delivery is not None and self.delivery != self.was_delivery) \
                or self.__original_amount != self.amount:
            _sum = 0
            if self.delivery is not None:
                _sum += self.delivery.price
            self.total_price = _sum

        if self.payment_status != self.__original_payment_status:
            if self.payment_status == self.PAYMENT_RECEIVED:
                self.current_status = self.STATUS_PAID
            elif self.payment_status == self.PAYMENT_AVAILABLE:
                self.current_status = self.STATUS_ONLINE_PAYMENT_AVAILABLE

        if self.current_status != self.__original_current_status:
            if self.current_status == self.STATUS_PAID:
                self.payment_status = self.PAYMENT_RECEIVED
            elif self.current_status == self.STATUS_ONLINE_PAYMENT_AVAILABLE:
                self.payment_status = self.PAYMENT_AVAILABLE
            else:
                self.payment_status = self.PAYMENT_UNAVAILABLE

        super(Order, self).save(*args, **kwargs)

        if self.payment_status != self.__original_payment_status:
            if self.payment_status == self.PAYMENT_AVAILABLE:
                send_email_user_notification(self.email, self, 'Avtopilot1.ru: Разрешена оплата заказа #%d' % self.pk,
                                             'messages/email_payment_available_notification.txt')
            elif self.payment_status == self.PAYMENT_RECEIVED:
                pass
                # TODO payment received email

        if self.__original_current_status != self.current_status:
            # TODO change email method
            send_email_user_notification(self.email, self, 'Avtopilot1.ru: Изменен статус заказа #%d' % self.pk,
                                         'messages/email_status_changed_notification.txt')

        self.__original_payment_status = self.payment_status
        self.__original_current_status = self.current_status
        self.__original_amount = self.amount


@receiver(payment_completed)
def payment_completed_callback(sender, **kwargs):
    try:
        # order = sender.paid_order.get()
        order = Order.objects.get(payment_id=sender.id)
        order.payment_status = Order.PAYMENT_RECEIVED
        order.save()

        send_email_user_notification('info@avtopilot1.ru', order, 'Заказ #%d оплачен' % order.pk,
                                     'messages/email_order_paid_notification.txt')
    except Exception:
        pass
