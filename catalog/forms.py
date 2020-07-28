from django import forms

from catalog.models import Material, Case


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['title', 'price', 'stock', 'colors', 'order', 'parent']
        widgets = {
            'colors': forms.SelectMultiple(attrs={
                'size': 25,
                'required': True,
                'label': 'Цвета',
                'class': 'input-xxlarge'
            })
        }


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = [field.name for field in Case._meta.fields]
        exclude = ('created', 'updated')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input-xxlarge'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'input-xxlarge'
            }),
            'tab_reviews': forms.SelectMultiple(attrs={
                'size': 25,
                'class': 'input-xxlarge'
            }),
            'qna': forms.SelectMultiple(attrs={
                'size': 25,
                'class': 'input-xxlarge'
            }),
            'accessories': forms.SelectMultiple(attrs={
                'size': 25,
                'class': 'input-xxlarge'
            })
        }


class OrderForm(forms.Form):
    name = forms.CharField(max_length=255, label='*Имя', widget=forms.TextInput({
        'placeholder': 'Иван',
        'id': 'order_id_name'
    }))
    last_name = forms.CharField(max_length=255, label='*Фамилия', widget=forms.TextInput({
        'placeholder': 'Иванов',
        'id': 'order_id_last_name'
    }))
    # middle_name = forms.CharField(max_length=255, label='Отчество', required=False)
    phone = forms.CharField(max_length=255, label='*Телефон', widget=forms.TextInput({
        'type': 'tel',
        'placeholder': '+7 (999) 999-99-99',
        'id': 'order_id_phone'
    }))
    email = forms.CharField(max_length=255, label='*E-mail', widget=forms.EmailInput({
        'placeholder': 'ivanov@gmail.com',
        'id': 'order_id_email'
    }))
    # country = forms.CharField(max_length=255, label='*Страна')
    address = forms.CharField(max_length=255, label='*Полный адрес доставки', widget=forms.TextInput({
        'placeholder': 'Россия, Москва, Ленинский проспект, 22, подъезд 3',
        'id': 'order_id_address'
    }))
    comment = forms.CharField(label='Комментарий', required=False, widget=forms.Textarea({
        'data-auto-expand': True,
        'data-max-height': 300,
        'rows': 3,
        'placeholder': 'Ваш комментарий ...',
        'id': 'order_id_comment'
    }))
    delivery = forms.BooleanField(label='Доставка', required=False, widget=forms.CheckboxInput({
        'id': 'order_id_delivery',
        'checked': True
    }))
