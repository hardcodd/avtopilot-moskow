from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.models import ContentType
from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField

from app.my_storage import MyStorage as Fs
from app.utils import fn
from django.urls import reverse


class Vacations(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(default='vacations', unique=True, verbose_name='Слаг')
    image = ThumbnailerImageField(verbose_name='Изображение', storage=Fs(), upload_to=fn, blank=True, null=True)
    content = RichTextUploadingField(verbose_name='Контент', blank=True, null=True)
    content_middle = RichTextUploadingField(verbose_name='Контент в середине', blank=True, null=True)
    # SEO
    seo_title = models.CharField(max_length=255, verbose_name='СЕО Заголовок', blank=True, null=True)
    meta_description = models.CharField(max_length=160, verbose_name='Мета описание', blank=True, null=True)
    meta_keywords = models.CharField(max_length=160, verbose_name='Ключевые слова', blank=True, null=True)
    meta_image = ThumbnailerImageField(verbose_name='Изображение для соц. сетей', storage=Fs(), upload_to=fn,
                                   blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'

    @property
    def panes(self):
        return self.pane_set.filter(publish=True).order_by('order')

    @property
    def accordion(self):
        return self.accordion_set.filter(publish=True).order_by('order')

    @staticmethod
    def get_absolute_url():
        return reverse('vacations')

    def get_edit_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))


class Pane(models.Model):
    publish = models.BooleanField(verbose_name='Опубликовано', default=False)
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Контент', blank=True, null=True)
    parent = models.ForeignKey(Vacations, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(verbose_name='Порядок', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Панели'


class Accordion(models.Model):
    publish = models.BooleanField(verbose_name='Опубликовано', default=False)
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = RichTextUploadingField(verbose_name='Контент', blank=True, null=True)
    parent = models.ForeignKey(Vacations, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(verbose_name='Порядок', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Аккордион'
