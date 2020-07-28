from django import forms

from comment.models import MainReview


class ReviewForm(forms.Form):
    CHOICES = ((5, 5), (4, 4), (3, 3), (2, 2), (1, 1))
    content_type = forms.CharField(widget=forms.HiddenInput)
    obj_id = forms.IntegerField(widget=forms.HiddenInput)
    rating = forms.IntegerField(widget=forms.RadioSelect(choices=CHOICES))
    content = forms.CharField(widget=forms.Textarea, label='Комментарий')


class MainReviewForm(forms.ModelForm):
    class Meta:
        model = MainReview
        fields = ['section', 'name', 'phone', 'email', 'video', 'image', 'content']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя и фамилия...', 'class': 'first_last_name'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Ваш телефон...', 'type': 'tel'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ваш E-mail...'}),
            'video': forms.URLInput(attrs={'placeholder': 'Ссылка на видео...'}),
            'image': forms.FileInput()
        }
