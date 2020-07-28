from django import forms


class TextUs(forms.Form):
    NAME = forms.CharField(max_length=100, label='Имя', required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Имя:',
        'id': 'id_NAME_1'
    }))
    PHONE_MOBILE = forms.CharField(max_length=20, label='Телефон', widget=forms.TextInput(attrs={
        'placeholder': 'Телефон:',
        'type': 'tel',
        'id': 'id_PHONE_1'
    }))
    EMAIL_WORK = forms.CharField(max_length=255, label='E-mail', required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'E-mail:'
    }))
    COMMENTS = forms.CharField(label='Сообщение', required=True, widget=forms.Textarea(attrs={
        'placeholder': 'Сообщение:',
        'class': 'auto-expand',
        'rows': 4,
        'data-min-rows': 4
    }))


class CallBack(forms.Form):
    NAME = forms.CharField(max_length=100, label='Имя', required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Имя:',
        'id': 'id_NAME_2'
    }))
    PHONE_MOBILE = forms.CharField(max_length=20, label='Телефон', widget=forms.TextInput(attrs={
        'placeholder': 'Телефон:',
        'type': 'tel',
        'id': 'id_PHONE_2'
    }))


class HomeInstallOrderForm(forms.Form):
    NAME = forms.CharField(max_length=100, label='Имя', required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Имя:',
        'id': 'id_NAME_3'
    }))
    PHONE_MOBILE = forms.CharField(max_length=20, label='Телефон', required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Телефон:',
        'type': 'tel',
        'id': 'id_PHONE_2'
    }))
