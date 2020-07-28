from adminsortable.models import SortableMixin
from django.db import models
import uuid

from easy_thumbnails.fields import ThumbnailerImageField
from app.my_storage import MyStorage as Fs
from app.utils import fn


class CaseBuilder(models.Model):
    slug = models.SlugField(unique=True, default='case-builder', editable=False)
    title = models.CharField(max_length=255, default='Конструктор чехлов', editable=False)
    # SEO
    seo_title = models.CharField(max_length=255, verbose_name='СЕО Заголовок', blank=True)
    meta_description = models.CharField(max_length=260, verbose_name='Мета описание', blank=True)
    meta_keywords = models.CharField(max_length=160, verbose_name='Ключевые слова', blank=True)
    meta_image = ThumbnailerImageField(verbose_name='Изображение для соц. сетей', storage=Fs(), upload_to=fn,
                                   blank=True, null=True)

    class Meta:
        verbose_name = 'Конструктор чехлов'
        verbose_name_plural = 'Конструктор чехлов'

    def __str__(self):
        return self.title


class MateBuilder(models.Model):
    slug = models.SlugField(unique=True, default='mate-builder', editable=False)
    title = models.CharField(max_length=255, default='Конструктор ковриков', editable=False)
    nameplate = models.PositiveSmallIntegerField(default=10, verbose_name='Максимальное количество шильдиков')
    nameplate_image = ThumbnailerImageField(verbose_name='Изображение шильдика', blank=True)
    bearing = ThumbnailerImageField(verbose_name='Изображение подпятника', blank=True)
    # price = models.PositiveIntegerField(verbose_name='Цена комплекта в салон', default=0)
    # price_trunk = models.PositiveIntegerField(verbose_name='Цена комплекта в багажник', default=0)
    nameplate_price = models.PositiveIntegerField(verbose_name='Цена за 1 шильдик', default=0)
    bearing_price = models.PositiveIntegerField(verbose_name='Цена за подпятник', default=0)
    set = models.TextField(verbose_name='Комплекты', help_text='Каждый комплект с новой строки<br>Пример: <название>|<цена>', blank=True)
    # SEO
    seo_title = models.CharField(max_length=255, verbose_name='СЕО Заголовок', blank=True)
    meta_description = models.CharField(max_length=260, verbose_name='Мета описание', blank=True)
    meta_keywords = models.CharField(max_length=160, verbose_name='Ключевые слова', blank=True)
    meta_image = ThumbnailerImageField(verbose_name='Изображение для соц. сетей', storage=Fs(), upload_to=fn,
                                   blank=True, null=True)

    class Meta:
        verbose_name = 'Конструктор ковриков'
        verbose_name_plural = 'Конструктор ковриков'

    def __str__(self):
        return self.title


class Type(SortableMixin):
    title = models.CharField(max_length=255, verbose_name='Название')
    parent = models.ForeignKey(CaseBuilder, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(default=0)
    uuid = models.UUIDField(editable=False, default=uuid.uuid4)

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'
        ordering = ['order']

    def __str__(self):
        return self.title


class Seam(SortableMixin):
    title = models.CharField(max_length=255, verbose_name='Название')
    price = models.PositiveSmallIntegerField(verbose_name='Цена', default='0')
    parent = models.ForeignKey(Type, verbose_name='Тип', on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(default=0)
    uuid = models.UUIDField(editable=False, default=uuid.uuid4)

    class Meta:
        verbose_name = 'Отстрочка'
        verbose_name_plural = 'Отстрочка (чехлы)'
        ordering = ['order']

    def __str__(self):
        return '%s - %s' % (self.title, self.parent.title)


class SeamColor(SortableMixin):
    title = models.CharField(max_length=255, verbose_name='Название')
    image = ThumbnailerImageField(verbose_name='Изображение')
    hex = models.CharField(max_length=7, verbose_name='Цвет', help_text='Пример: #a4a4a4')
    order = models.PositiveSmallIntegerField(default=0)
    parent = models.ForeignKey(Seam, verbose_name='Отстрочка', on_delete=models.CASCADE)
    uuid = models.UUIDField(editable=False, default=uuid.uuid4)

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвет отстрочки'
        ordering = ['order']

    def __str__(self):
        return '%s - %s' % (self.title, self.parent.title)


class MateSeamColor(SortableMixin):
    title = models.CharField(max_length=255, verbose_name='Название')
    hex = models.CharField(max_length=7, verbose_name='Цвет', help_text='Пример: #a4a4a4')
    order = models.PositiveSmallIntegerField(default=0)
    parent = models.ForeignKey(MateBuilder, verbose_name='Отстрочка', on_delete=models.CASCADE)
    uuid = models.UUIDField(editable=False, default=uuid.uuid4)

    class Meta:
        verbose_name = 'Цвет канта'
        verbose_name_plural = 'Цвета канта'
        ordering = ['order']

    def __str__(self):
        return '%s - %s' % (self.title, self.parent.title)


class Material(SortableMixin):
    title = models.CharField(max_length=255, verbose_name='Название')
    order = models.PositiveSmallIntegerField(default=0)
    parent = models.ForeignKey(Type, verbose_name='Тип', on_delete=models.CASCADE)
    price = models.PositiveSmallIntegerField(verbose_name='Цена', default='0')
    uuid = models.UUIDField(editable=False, default=uuid.uuid4)

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы (чехлы)'
        ordering = ['order']

    def __str__(self):
        return '%s - %s' % (self.title, self.parent.title)


class Color(SortableMixin):
    title = models.CharField(max_length=255, verbose_name='Название')
    image = ThumbnailerImageField(verbose_name='Изображение')
    hex = models.CharField(max_length=7, verbose_name='Цвет', help_text='Пример: #a4a4a4')
    order = models.PositiveSmallIntegerField(default=0)
    parent = models.ForeignKey(Material, verbose_name='Материал', on_delete=models.CASCADE)
    uuid = models.UUIDField(editable=False, default=uuid.uuid4)

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'
        ordering = ['order']

    def __str__(self):
        return '%s - %s' % (self.title, self.parent.title)


class MateColor(SortableMixin):
    title = models.CharField(max_length=255, verbose_name='Название')
    image = ThumbnailerImageField(verbose_name='Изображение')
    order = models.PositiveSmallIntegerField(default=0)
    parent = models.ForeignKey(MateBuilder, verbose_name='Материал', on_delete=models.CASCADE)
    uuid = models.UUIDField(editable=False, default=uuid.uuid4)

    class Meta:
        verbose_name = 'Цвет коврика'
        verbose_name_plural = 'Цвета коврика'
        ordering = ['order']

    def __str__(self):
        return '%s - %s' % (self.title, self.parent.title)


class Base(SortableMixin):
    title = models.CharField(max_length=255, verbose_name='Название')
    image = ThumbnailerImageField(verbose_name='Изображение')
    hex = models.CharField(max_length=7, verbose_name='Цвет', help_text='Пример: #a4a4a4')
    order = models.PositiveSmallIntegerField(default=0)
    parent = models.ForeignKey(Type, on_delete=models.CASCADE)
    price = models.PositiveSmallIntegerField(verbose_name='Цена', default='0')
    uuid = models.UUIDField(editable=False, default=uuid.uuid4)

    class Meta:
        verbose_name = 'Основа'
        verbose_name_plural = 'Основы (чехлы)'
        ordering = ['order']

    def __str__(self):
        return '%s - %s' % (self.title, self.parent.title)


class Rear(SortableMixin):
    title = models.CharField(max_length=255, verbose_name='Название')
    image = ThumbnailerImageField(verbose_name='Изображение')
    hex = models.CharField(max_length=7, verbose_name='Цвет', help_text='Пример: #a4a4a4')
    order = models.PositiveSmallIntegerField(default=0)
    parent = models.ForeignKey(Type, on_delete=models.CASCADE)
    uuid = models.UUIDField(editable=False, default=uuid.uuid4)

    class Meta:
        verbose_name = 'Тыл'
        verbose_name_plural = 'Тылы (чехлы)'
        ordering = ['order']

    def __str__(self):
        return '%s - %s' % (self.title, self.parent.title)
