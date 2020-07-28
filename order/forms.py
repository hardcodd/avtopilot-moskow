from django import forms
from yandex_money.models import Payment


class PaymentForm(forms.Form):
    payment_types = (
        ('PC', 'Кошелек Яндекс.Деньги'),
        ('AC', 'Банковская карта'),
        ('GP', 'Наличными через кассы и терминалы'),
        # ('MC', 'Счет мобильного телефона'),
        # ('WM', 'Кошелек WebMoney'),
        ('SB', 'Сбербанк: оплата по SMS или Сбербанк Онлайн'),
        ('AB', 'Альфа-Клик'),
        ('MA', 'MasterPass'),
        ('PB', 'Интернет-банк Промсвязьбанка'),
        ('QW', 'QIWI Wallet'),
        ('CR', 'Заплатить по частям')
    )

    shopId = forms.CharField(label='shopId', widget=forms.TextInput({'type': 'hidden'}))
    scid = forms.CharField(label='scid', widget=forms.TextInput({'type': 'hidden'}))
    sum = forms.CharField(label='sum', widget=forms.TextInput({'type': 'hidden'}))
    customerNumber = forms.CharField(label='customerNumber', widget=forms.TextInput({'type': 'hidden'}))
    orderNumber = forms.CharField(label='orderNumber', widget=forms.TextInput({'type': 'hidden'}))
    paymentType = forms.CharField(label='Способ оплаты', widget=forms.Select(choices=payment_types))
    ym_merchant_receipt = forms.CharField(label='ym_merchant_receipt', widget=forms.TextInput({'type': 'hidden'}))

