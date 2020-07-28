from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField

from catalog.models import UniversalProduct


class General(models.Model):
    # SEO
    title = models.CharField(max_length=255, verbose_name='Заголовок сайта', blank=True)
    title_part = models.CharField(max_length=255, verbose_name='Вторая часть заголовка', blank=True)
    divider = models.CharField(max_length=3, verbose_name='Разделитель заголовка', blank=True)
    keywords = models.CharField(max_length=255, verbose_name='Ключевые слова', blank=True)
    description = models.CharField(max_length=255, verbose_name='Описание', blank=True)
    meta_image = ThumbnailerImageField(verbose_name='Изображение для соц.сетей', blank=True)
    order = models.PositiveIntegerField(blank=True, null=True)

    # Contacts
    phone_free = models.CharField(max_length=255, verbose_name='Телефон бесплатной линии', blank=True)
    phone = models.CharField(max_length=255, verbose_name='Телефон', blank=True)
    email = models.EmailField(verbose_name='E-mail', blank=True)
    city = models.CharField(max_length=255, verbose_name='Город', blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', blank=True)
    zip = models.CharField(max_length=255, verbose_name='Индекс', blank=True)
    work_time = models.CharField(max_length=255, verbose_name='Время работы', blank=True)
    work_time_header = models.CharField(max_length=255, verbose_name='Время работы в шапке', blank=True)
    map = models.TextField(verbose_name='Карта', blank=True, null=True)

    # Accessories
    accessories = models.ManyToManyField(UniversalProduct, verbose_name='Аксессуары', blank=True, related_name='common_accessories')

    def __str__(self):
        return 'Основное ID:%s' % (self.id,)

    class Meta:
        verbose_name = 'Опции сайта'
        verbose_name_plural = 'Опции сайта'

    def social(self):
        return self.social_set.filter(publish=True).order_by('order')


class Moderator(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField()
    active = models.BooleanField(default=True, verbose_name='Активный')
    parent = models.ForeignKey(General, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(blank=True, null=True)


class BlogWidget(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок виджета', blank=True)
    image = models.ImageField(verbose_name='Изображение')
    image_title = models.CharField(max_length=255, verbose_name='title')
    url = models.CharField(max_length=255, verbose_name='Ссылка', help_text='URL will be opened in a new tab but URI in the same tab.')
    parent = models.ForeignKey(General, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(blank=True, null=True)

    @property
    def is_external(self):
        return True if 'http://' in self.url or 'https://' in self.url else False


class Social(models.Model):
    publish = models.BooleanField(verbose_name='Опубликовано', default=True)
    link = models.URLField(verbose_name='Ссылка')
    icon = models.CharField(
        max_length=255,
        verbose_name='Иконка',
        help_text='<code><a href="https://fontawesome.com/icons?d=gallery&s=brands" '
                  'target="blank">FontAwesome</a></code>')
    parent = models.ForeignKey(General, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Соц.сеть'
        verbose_name_plural = 'Соц.сети'

    def __str__(self):
        return self.link.split('//')[-1].split('/')[0]
