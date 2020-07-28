from adminsortable.models import SortableMixin
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Min
from django.urls import reverse
from easy_thumbnails.fields import ThumbnailerImageField
from mptt.models import MPTTModel
from ckeditor_uploader.fields import RichTextUploadingField

from app import settings
from comment.utils import get_reviews, total_rating


def get_product_types():
    return (
        ('ACCESSORY', 'Аксессуары'),
        ('MATE', 'Автоковрики'),
        ('CAPE', 'Автонакидки'),
        ('BRAID', 'Оплётки')
    )


class Install(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = RichTextUploadingField(verbose_name='Контент', blank=True, null=True)
    order = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Где установить'
        verbose_name_plural = 'Где установить'


class Stock(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = RichTextUploadingField(verbose_name='Контент', blank=True, null=True)
    order = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Наличие в магазинах'
        verbose_name_plural = 'Наличие в магазинах'


class Make(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, verbose_name='Слаг', unique=True)
    image = ThumbnailerImageField(verbose_name='Изображение (500x296)', blank=True, null=True)
    video = models.URLField(max_length=255, verbose_name='Ссылка на видео', blank=True, null=True)
    title_description = models.CharField(max_length=255, verbose_name='Заголовок описания', blank=True, null=True)
    description = RichTextUploadingField(verbose_name='Описание', blank=True, null=True)
    order = models.PositiveIntegerField(blank=True, null=True)
    # SEO
    seo_title = models.CharField(max_length=255, verbose_name='СЕО Заголовок', blank=True, null=True)
    meta_description = models.CharField(max_length=260, verbose_name='Мета описание', blank=True, null=True)
    meta_keywords = models.CharField(max_length=160, verbose_name='Ключевые слова', blank=True, null=True)
    meta_image = ThumbnailerImageField(verbose_name='Изображение для соц. сетей',
                                   blank=True, null=True)

    class Meta:
        verbose_name = 'Марка'
        verbose_name_plural = 'Марки'

    class MPTTMeta:
        order_insertion_by = ['title']

    def get_edit_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

    def __str__(self):
        return self.title


class Model(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    make = models.ForeignKey(Make, verbose_name='Марка', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(verbose_name='Порядок', blank=True, null=True)

    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'
        ordering = ['order']

    def __str__(self):
        return '%s - %s' % (self.make, self.title)


class Guarantee(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    period = models.CharField(max_length=255, verbose_name='Срок действия')
    slug = models.SlugField(max_length=255, verbose_name='Слаг', unique=True)
    content = RichTextUploadingField(verbose_name='Контент', blank=True, null=True)
    order = models.PositiveIntegerField(blank=True, null=True)
    # SEO
    seo_title = models.CharField(max_length=255, verbose_name='СЕО Заголовок', blank=True, null=True)
    meta_description = models.CharField(max_length=260, verbose_name='Мета описание', blank=True, null=True)
    meta_keywords = models.CharField(max_length=160, verbose_name='Ключевые слова', blank=True, null=True)
    meta_image = ThumbnailerImageField(verbose_name='Изображение для соц. сетей',
                                   blank=True, null=True)

    class Meta:
        verbose_name = 'Гарантия'
        verbose_name_plural = 'Гарантии'

    def __str__(self):
        return '%s - %s' % (self.title, self.period)


class Reviews(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    image = ThumbnailerImageField(verbose_name='Изображение', blank=True, null=True)
    slug = models.SlugField(max_length=255, verbose_name='Слаг', unique=True)
    video = models.URLField(max_length=255, verbose_name='Ссылка на видео', blank=True, null=True)
    content = RichTextUploadingField(verbose_name='Контент', blank=True, null=True)
    order = models.PositiveIntegerField(blank=True, null=True)
    # SEO
    seo_title = models.CharField(max_length=255, verbose_name='СЕО Заголовок', blank=True, null=True)
    meta_description = models.CharField(max_length=260, verbose_name='Мета описание', blank=True, null=True)
    meta_keywords = models.CharField(max_length=160, verbose_name='Ключевые слова', blank=True, null=True)
    meta_image = ThumbnailerImageField(verbose_name='Изображение для соц. сетей',
                                   blank=True, null=True)

    @property
    def get_content(self):
        content = self.content
        if len(content) > 800:
            content = content[:800]
        return '%s%s' % (content, '...')

    def get_absolute_url(self):
        return reverse('review_detail', args=[str(self.slug)])

    class Meta:
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'

    def __str__(self):
        return self.title


class QnA(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = RichTextUploadingField(verbose_name='Контент', blank=True, null=True)
    order = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопрос - Ответ'

    def __str__(self):
        return self.title


class UniversalCategory(models.Model):
    PRODUCT_TYPES = get_product_types()
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, verbose_name='Слаг', unique=True)
    image = ThumbnailerImageField(verbose_name='Изображение (800x450)', blank=True, null=True)
    products_type = models.CharField(max_length=20, verbose_name='Тип товаров', choices=PRODUCT_TYPES)
    order = models.PositiveIntegerField(verbose_name='Порядок', blank=True, null=True)
    # SEO
    seo_title = models.CharField(max_length=255, verbose_name='СЕО Заголовок', blank=True)
    meta_description = models.CharField(max_length=260, verbose_name='Мета описание', blank=True)
    meta_keywords = models.CharField(max_length=160, verbose_name='Ключевые слова', blank=True)
    meta_image = ThumbnailerImageField(verbose_name='Изображение для соц. сетей',
                                   blank=True, null=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории товаров'
        ordering = ['order']

    def __str__(self):
        return self.title


class UniversalProduct(models.Model):
    STATUS_CHOICES = (('DRAFT', 'Черновик'), ('PUBLIC', 'Опубликованно'))
    PRODUCT_TYPES = get_product_types()
    status = models.CharField(max_length=20, verbose_name='Статус', choices=STATUS_CHOICES, default='DRAFT')
    product_type = models.CharField(max_length=20, verbose_name='Тип товара', choices=PRODUCT_TYPES, default='ACCESSORY')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, verbose_name='Слаг', unique=True)
    category = models.ForeignKey(UniversalCategory, verbose_name='Категория', on_delete=models.CASCADE)
    image = ThumbnailerImageField(verbose_name='Изображение (800x450)', blank=True, null=True)
    info = models.CharField(max_length=100, verbose_name='Доп. инфо', blank=True, null=True)
    views = models.IntegerField(verbose_name='Просмотров', default=0)
    weight = models.FloatField(verbose_name='Вес товара (кг)', blank=True, null=True)
    current_day = models.DateField(null=True)
    video = models.URLField(max_length=255, verbose_name='Ссылка на видео', blank=True, null=True)
    guarantee = models.ForeignKey(Guarantee, verbose_name='Гарантия', blank=True, null=True, on_delete=models.CASCADE)
    description = RichTextUploadingField(verbose_name='Описание', blank=True, null=True)
    tab_reviews = models.ManyToManyField(Reviews, verbose_name='Обзоры', blank=True)
    qna = models.ManyToManyField(QnA, verbose_name='Вопрос - Ответ', blank=True)
    accessories = models.ManyToManyField('self', verbose_name='Аксессуары', blank=True)
    install = models.ForeignKey(Install, verbose_name='Установка', blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name='Добавлено')
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name='Обновлено')
    order = models.PositiveIntegerField(blank=True, null=True)
    # SEO
    seo_title = models.CharField(max_length=255, verbose_name='СЕО Заголовок', blank=True, null=True)
    meta_description = models.CharField(max_length=260, verbose_name='Мета описание', blank=True, null=True)
    meta_keywords = models.CharField(max_length=160, verbose_name='Ключевые слова', blank=True, null=True)
    meta_image = ThumbnailerImageField(verbose_name='Изображение для соц. сетей',
                                   blank=True, null=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title

    @property
    def back_link(self):
        # For Breadcrumbs
        if self.product_type == 'ACCESSORY':
            return 'accessories'
        elif self.product_type == 'MATE':
            return 'mates'
        elif self.product_type == 'CAPE':
            return 'capes'
        elif self.product_type == 'BRAID':
            return 'braids'

    @property
    def back_title(self):
        # For Breadcrumbs
        if self.product_type == 'ACCESSORY':
            return 'Аксессуары'
        elif self.product_type == 'MATE':
            return 'Автоковрики'
        elif self.product_type == 'CAPE':
            return 'Автонакидки'
        elif self.product_type == 'BRAID':
            return 'Оплётки'

    @property
    def get_cls(self):
        return self.__class__.__name__.lower()

    @property
    def reviews(self):
        return get_reviews(self)

    @property
    def total_rating(self):
        return total_rating(self)

    @property
    def sizes(self):
        qs = UniversalSize.objects.filter(parent=self.pk).order_by('order')
        return qs

    @property
    def price(self):
        qs = self.sizes
        price = qs.aggregate(Min('price'))['price__min'] or None
        if qs.count() > 1:
            price = 'от %s' % (price,)
        return price

    @property
    def d_price(self):
        qs = self.sizes
        price = qs.aggregate(Min('price'))['price__min'] or None
        return price

    @property
    def get_content_type(self):
        content_type = ContentType.objects.get_for_model(self).model
        return content_type

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.slug)])

    def get_edit_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))


class Case(models.Model):
    STATUS_CHOICES = (('DRAFT', 'Черновик'), ('PUBLIC', 'Опубликованно'))
    status = models.CharField(max_length=20, verbose_name='Статус', choices=STATUS_CHOICES, default='DRAFT')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, verbose_name='Слаг', unique=True)
    model = models.ForeignKey(Model, verbose_name='Модель', on_delete=models.CASCADE)
    image = ThumbnailerImageField(verbose_name='Кузов (180x110)', blank=True, null=True)
    install_price = models.PositiveIntegerField(verbose_name='Цена за установку', blank=True, null=True)
    info = models.CharField(max_length=100, verbose_name='Доп. инфо', blank=True, null=True)
    views = models.IntegerField(verbose_name='Просмотров', default=0)
    weight = models.FloatField(verbose_name='Вес товара (кг)', blank=True, null=True)
    current_day = models.DateField(null=True)
    video = models.URLField(max_length=255, verbose_name='Ссылка на видео', blank=True, null=True)
    guarantee = models.ForeignKey(Guarantee, verbose_name='Гарантия', blank=True, null=True, on_delete=models.CASCADE)
    description = RichTextUploadingField(verbose_name='Описание', blank=True, null=True)
    install = models.ForeignKey(Install, verbose_name='Установка', blank=True, null=True, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, verbose_name='Наличие в магазинах', blank=True, null=True,
                              on_delete=models.CASCADE)
    code = models.CharField(max_length=50, verbose_name='Часть артикула', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name='Добавлено')
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name='Обновлено')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Пользователь', default=1, on_delete=models.CASCADE)
    tab_reviews = models.ManyToManyField(Reviews, verbose_name='Обзоры', blank=True)
    qna = models.ManyToManyField(QnA, verbose_name='Вопрос - Ответ', blank=True)
    accessories = models.ManyToManyField(UniversalProduct, verbose_name='Аксессуары', blank=True)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)
    # SEO
    seo_title = models.CharField(max_length=255, verbose_name='СЕО Заголовок', blank=True, null=True)
    meta_description = models.CharField(max_length=260, verbose_name='Мета описание', blank=True, null=True)
    meta_keywords = models.CharField(max_length=160, verbose_name='Ключевые слова', blank=True, null=True)
    meta_image = ThumbnailerImageField(verbose_name='Изображение для соц. сетей',
                                   blank=True, null=True)

    class Meta:
        verbose_name = 'Чехол'
        verbose_name_plural = 'Чехлы'

    def __str__(self):
        return self.title

    @property
    def get_cls(self):
        return self.__class__.__name__.lower()

    @property
    def reviews(self):
        return get_reviews(self)

    @property
    def total_rating(self):
        return total_rating(self)

    @property
    def get_content_type(self):
        content_type = ContentType.objects.get_for_model(self).model
        return content_type

    def get_absolute_url(self):
        return reverse('case_detail', args=[str(self.slug)])

    def get_edit_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))


class Color(models.Model):
    code = models.CharField(max_length=50, verbose_name='Часть артикула', blank=True, null=True)
    material_name = models.CharField(max_length=255, verbose_name='Материал')
    color_name = models.CharField(max_length=255, verbose_name='Цвет')
    image = ThumbnailerImageField(verbose_name='Миниатюра (30x40)', blank=True, null=True)
    big_image = ThumbnailerImageField(verbose_name='Превью (386x386)', blank=True, null=True)
    video = models.FileField(verbose_name='Видео превью', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'
        ordering = ['order']

    def __str__(self):
        return '%s - %s' % (self.material_name, self.color_name)


class Material(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    price = models.IntegerField(verbose_name='Цена')
    stock = models.BooleanField(verbose_name='Только под заказ', default=False, blank=True, null=True)
    colors = models.ManyToManyField(Color, verbose_name='Цвета')
    order = models.PositiveIntegerField(blank=True, null=True)
    parent = models.ForeignKey(Case, verbose_name='Чехол', blank=True, null=True,
                               on_delete=models.CASCADE, related_name='children_materials')

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'
        ordering = ['order']

    def get_colors(self):
        return self.colors.all().order_by('order')

    def __str__(self):
        return self.title


class Image(models.Model):
    image = ThumbnailerImageField(verbose_name='Изображение')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    alt = models.CharField(max_length=255, verbose_name='Альт')
    order = models.IntegerField(verbose_name='Порядок', default=0)
    parent = models.ForeignKey(Case, verbose_name='Чехол', blank=True, null=True,
                               on_delete=models.CASCADE, related_name='children_images')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Галлерея'

    def __str__(self):
        return self.title


class UniversalImage(models.Model):
    image = ThumbnailerImageField(verbose_name='Изображение')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    alt = models.CharField(max_length=255, verbose_name='Альт')
    order = models.IntegerField(verbose_name='Порядок', default=0)
    parent = models.ForeignKey(UniversalProduct, verbose_name='Аксессуар', blank=True, null=True,
                               on_delete=models.CASCADE, related_name='children_images')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Галлерея'

    def __str__(self):
        return self.title


class UniversalSize(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    price = models.IntegerField(verbose_name='Цена')
    stock = models.BooleanField(verbose_name='Только под заказ', default=False, blank=True, null=True)
    order = models.IntegerField(verbose_name='Порядок', default=0)
    parent = models.ForeignKey(UniversalProduct, verbose_name='Аксессуар', blank=True, null=True,
                               on_delete=models.CASCADE, related_name='children_sizes')

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'

    def __str__(self):
        return self.title


class UniversalColor(models.Model):
    color_name = models.CharField(max_length=255, verbose_name='Цвет')
    image = ThumbnailerImageField(verbose_name='Миниатюра (50x65)', blank=True, null=True)
    big_image = ThumbnailerImageField(verbose_name='Превью (386x386)', blank=True, null=True)
    order = models.IntegerField(verbose_name='Порядок', default=0)
    parent = models.ForeignKey(UniversalProduct, verbose_name='Аксессуар', blank=True, null=True,
                               on_delete=models.CASCADE, related_name='children_colors')

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'

    def __str__(self):
        return self.color_name


class CatalogPage(models.Model):
    MODELS = (
        ('MAKE', 'Марки'),
        ('ACCESSORIES', 'Аксессуары'),
        ('MATES', 'Коврики'),
        ('CAPES', 'Накидки'),
        ('BRAIDS', 'Оплётки')
    )
    model = models.CharField(max_length=20, verbose_name='Что выводить', choices=MODELS, default='DRAFT')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, verbose_name='Слаг', unique=True)
    video = models.URLField(max_length=255, verbose_name='Ссылка на видео', blank=True, null=True)
    title_description = models.CharField(max_length=255, verbose_name='Заголовок описания', blank=True, null=True)
    description = RichTextUploadingField(verbose_name='Описание', blank=True, null=True)
    order = models.PositiveIntegerField(blank=True, null=True)
    # SEO
    seo_title = models.CharField(max_length=255, verbose_name='СЕО Заголовок', blank=True, null=True)
    meta_description = models.CharField(max_length=260, verbose_name='Мета описание', blank=True, null=True)
    meta_keywords = models.CharField(max_length=160, verbose_name='Ключевые слова', blank=True, null=True)
    meta_image = ThumbnailerImageField(verbose_name='Изображение для соц. сетей',
                                   blank=True, null=True)

    class Meta:
        verbose_name = 'Страница каталога'
        verbose_name_plural = 'Страницы каталога'

    def __str__(self):
        return self.title

    def get_edit_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))


class PromoCode(models.Model):
    code = models.CharField(max_length=20, verbose_name='Промокод', help_text='До 20ти символов!')
    percent = models.PositiveSmallIntegerField(verbose_name='Скидка в %')

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'

    def __str__(self):
        return self.code
