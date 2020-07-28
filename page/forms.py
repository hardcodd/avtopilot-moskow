from django import forms


class PartnerForm(forms.Form):
    PHONE_MOBILE = forms.CharField(max_length=20, label='Телефон', widget=forms.TextInput(attrs={
        'placeholder': 'Телефон:',
        'type': 'tel'
    }))


class BecomePartnerForm(forms.Form):
    NAME = forms.CharField(max_length=100, label='Имя', widget=forms.TextInput(attrs={
        'placeholder': 'Имя:',
        'type': 'text'
    }))
    PHONE_MOBILE = forms.CharField(max_length=20, label='Телефон', widget=forms.TextInput(attrs={
        'placeholder': 'Телефон:',
        'type': 'tel'
    }))
    EMAIL_WORK = forms.CharField(max_length=100, label='E-mail', widget=forms.EmailInput(attrs={
        'placeholder': 'E-mail:',
        'type': 'email'
    }))
    ADDRESS = forms.CharField(max_length=50, label='Город', widget=forms.TextInput(attrs={
        'placeholder': 'Город:',
        'type': 'text'
    }))
    COMMENTS = forms.CharField(max_length=500, label='Комментарий', widget=forms.Textarea(attrs={
        'placeholder': 'Комментарий:',
        'data-auto-expand': '',
        'data-max-height': '500',
        'rows': '4'
    }))


class InlineForm(forms.Form):
    NAME = forms.CharField(max_length=100, label='Имя', widget=forms.TextInput(attrs={
        'placeholder': 'Имя:',
        'type': 'text'
    }))
    PHONE_MOBILE = forms.CharField(max_length=20, label='Телефон', widget=forms.TextInput(attrs={
        'placeholder': 'Телефон:',
        'type': 'tel'
    }))


class StaffMemberForm(forms.Form):
    NAME = forms.CharField(max_length=100, label='Имя', required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Имя:'
    }))
    PHONE_MOBILE = forms.CharField(max_length=20, label='Телефон', required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Телефон:',
        'type': 'tel'
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


class ContactForm(forms.Form):
    NAME = forms.CharField(max_length=100, label='Имя', widget=forms.TextInput(attrs={
        'placeholder': 'Имя:'
    }))
    PHONE_MOBILE = forms.CharField(max_length=20, label='Телефон', widget=forms.TextInput(attrs={
        'placeholder': 'Телефон:',
        'type': 'tel'
    }))
    EMAIL_WORK = forms.CharField(max_length=255, label='E-mail', widget=forms.EmailInput(attrs={
        'placeholder': 'E-mail:'
    }))
    COMMENTS = forms.CharField(label='Сообщение', required=False, widget=forms.Textarea(attrs={
        'placeholder': 'Сообщение:',
        'class': 'auto-expand',
        'rows': 4,
        'data-min-rows': 4
    }))


class ConsultationForm(forms.Form):
    NAME = forms.CharField(max_length=100, label='Имя', widget=forms.TextInput(attrs={
        'placeholder': 'Имя:'
    }))
    PHONE_MOBILE = forms.CharField(max_length=20, label='Телефон', widget=forms.TextInput(attrs={
        'placeholder': 'Телефон:',
        'type': 'tel'
    }))
    COMMENTS = forms.CharField(label='Сообщение', required=False, widget=forms.Textarea(attrs={
        'placeholder': 'Сообщение:',
        'class': 'auto-expand',
        'rows': 4,
        'data-min-rows': 4
    }))


class AboutForm(forms.ModelForm):
    title = \
        forms.CharField(max_length=255, label='Заголовок', widget=forms.TextInput(attrs={
            'class': 'input-xxlarge'
        }))
    slug = \
        forms.SlugField(max_length=255,  label='Слаг', widget=forms.TextInput(attrs={
            'class': 'input-xxlarge'
        }))
    seo_title = \
        forms.CharField(max_length=255, label='СЕО заголовок', required=False, widget=forms.TextInput(attrs={
            'class': 'input-xxlarge'
        }))
    meta_description = \
        forms.CharField(max_length=255, label='Мета описание', required=False, widget=forms.TextInput(attrs={
            'class': 'input-xxlarge'
        }))
    meta_keywords = \
        forms.CharField(max_length=255, label='Ключевые слова', required=False, widget=forms.TextInput(attrs={
            'class': 'input-xxlarge'
        }))


class HelpForm(forms.ModelForm):
    title = \
        forms.CharField(max_length=255, label='Заголовок', widget=forms.TextInput(attrs={
            'class': 'input-xxlarge'
        }))
    slug = \
        forms.SlugField(max_length=255,  label='Слаг', widget=forms.TextInput(attrs={
            'class': 'input-xxlarge'
        }))
    seo_title = \
        forms.CharField(max_length=255, label='СЕО заголовок', required=False, widget=forms.TextInput(attrs={
            'class': 'input-xxlarge'
        }))
    meta_description = \
        forms.CharField(max_length=255, label='Мета описание', required=False, widget=forms.TextInput(attrs={
            'class': 'input-xxlarge'
        }))
    meta_keywords = \
        forms.CharField(max_length=255, label='Ключевые слова', required=False, widget=forms.TextInput(attrs={
            'class': 'input-xxlarge'
        }))


class HelpItemForm(forms.ModelForm):
    title = \
        forms.CharField(max_length=255, label='Заголовок', widget=forms.TextInput(attrs={
            'class': 'input-xxlarge'
        }))


class TabItemForm(forms.ModelForm):
    title = \
        forms.CharField(max_length=255, label='Заголовок', widget=forms.TextInput(attrs={
            'class': 'input-xxlarge'
        }))


class TabSectionForm(forms.ModelForm):
    title = \
        forms.CharField(max_length=255, label='Заголовок', widget=forms.TextInput(attrs={
            'class': 'input-xxlarge'
        }))


class PortfolioWorkForm(forms.ModelForm):
    title = \
        forms.CharField(max_length=255, label='Заголовок', widget=forms.TextInput(attrs={
            'class': 'input-xxlarge'
        }))
    caption = \
        forms.CharField(max_length=255, label='Описание', required=False, widget=forms.TextInput(attrs={
            'class': 'input-xxlarge'
        }))
