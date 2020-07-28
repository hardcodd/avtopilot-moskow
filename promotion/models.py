import datetime

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from easy_thumbnails.fields import ThumbnailerImageField

from app.my_storage import MyStorage as Fs
from app.utils import fn, video_url, video_image, lost_time
from comment.utils import total_rating, get_reviews


class PromotionPage(models.Model):
    published = models.BooleanField(verbose_name='Опубликованно', default=True)
    title = models.CharField(verbose_name='Заголовок', max_length=255)
    slug = models.SlugField(verbose_name='Слаг', max_length=255, unique=True, default='promotion')
    order = models.PositiveIntegerField(blank=True, null=True)
    # SEO
    seo_title = models.CharField(max_length=255, verbose_name='СЕО Заголовок', blank=True, null=True)
    meta_description = models.CharField(max_length=160, verbose_name='Мета описание', blank=True, null=True)
    meta_keywords = models.CharField(max_length=160, verbose_name='Ключевые слова', blank=True, null=True)
    meta_image = ThumbnailerImageField(verbose_name='Изображение для соц. сетей', storage=Fs(), upload_to=fn,
                                   blank=True, null=True)

    class Meta:
        verbose_name = 'Каталог акций'
        verbose_name_plural = 'Каталог акций'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('promotion', args=[str(self.slug)])

    def __str__(self):
        return self.title

    def get_edit_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))


class Category(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=255)
    widget_title = models.CharField(verbose_name='Заголовок виджета', max_length=255, blank=True, null=True)
    slug = models.SlugField(verbose_name='Слаг', max_length=255, unique=True)
    order = models.PositiveIntegerField(blank=True, null=True)
    # SEO
    seo_title = models.CharField(max_length=255, verbose_name='СЕО Заголовок', blank=True, null=True)
    meta_description = models.CharField(max_length=160, verbose_name='Мета описание', blank=True, null=True)
    meta_keywords = models.CharField(max_length=160, verbose_name='Ключевые слова', blank=True, null=True)
    meta_image = ThumbnailerImageField(verbose_name='Изображение для соц. сетей', storage=Fs(), upload_to=fn,
                                   blank=True, null=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('promotion_category', args=[str(self.slug)])

    def get_edit_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))


class Promotion(models.Model):
    published = models.BooleanField(verbose_name='Опубликованно', default=True)
    title = models.CharField(verbose_name='Заголовок', max_length=255)
    slug = models.SlugField(verbose_name='Слаг', max_length=255, unique=True)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    image = ThumbnailerImageField(verbose_name='Изображение (500x296)', storage=Fs(), upload_to=fn, blank=True, null=True)
    video = models.URLField(verbose_name='Ссылка на видео', blank=True,
                            help_text='Выводится кнопкой при наведении на миниатюру.')
    price = models.PositiveIntegerField(verbose_name='Цена', blank=True, null=True)
    discounted = models.PositiveIntegerField(verbose_name='Цена со скидкой', blank=True, null=True)
    time_end = models.DateTimeField(verbose_name='Окончание акции', blank=True, null=True)
    order = models.PositiveIntegerField(blank=True, null=True)
    # SEO
    seo_title = models.CharField(max_length=255, verbose_name='СЕО Заголовок', blank=True, null=True)
    meta_description = models.CharField(max_length=160, verbose_name='Мета описание', blank=True, null=True)
    meta_keywords = models.CharField(max_length=160, verbose_name='Ключевые слова', blank=True, null=True)
    meta_image = ThumbnailerImageField(verbose_name='Изображение для соц. сетей', storage=Fs(), upload_to=fn,
                                   blank=True, null=True)

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('promotion_detail', args=[str(self.slug)])

    def __str__(self):
        return self.title

    @property
    def video_url(self):
        return video_url(self.video)

    @property
    def video_image(self):
        return video_image(self.video)

    @property
    def to_end(self):
        return lost_time(self.time_end)

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
        instance = self
        content_type = ContentType.objects.get_for_model(instance).model
        return content_type

    @property
    def slider(self):
        return self.slides.all().order_by('order')

    @property
    def accordion(self):
        return self.accordion_items.all().order_by('order')

    @property
    def get_discount(self):
        price = self.price
        discounted = self.discounted
        percent = ''
        if price and discounted:
            percent = '{:.2f}'.format(discounted / price * 100 - 100)
            if int(str(percent).split('.')[1]) == 0:
                percent = int(str(percent).split('.')[0])
        if not percent:
            return ''
        return '{}%'.format(percent)

    def get_edit_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

    @property
    def get_price(self):
        price = self.price
        discounted = self.discounted
        discount = self.get_discount
        output = ''
        if discount:
            output = '<span class="price-span"><s>{} руб.</s></span>&nbsp;-&nbsp;<span class="price-discount">{} руб.' \
                     '</span><span class="percent">{}</span>'.format(price, discounted, discount)
        elif price:
            output = '<span class="price-span">%s руб.</span>' % price
        return mark_safe(output)


class Slide(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    video = models.URLField(verbose_name='Ссылка на видео', blank=True)
    image = ThumbnailerImageField(verbose_name='Изображение (1110x390)', blank=True)
    parent = models.ForeignKey(Promotion, on_delete=models.CASCADE, related_name='slides')
    order = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайды'

    @property
    def video_url(self):
        return video_url(self.video)

    @property
    def video_image(self):
        return video_image(self.video)


class Accordion(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = RichTextUploadingField(verbose_name='Контент', blank=True, null=True)
    parent = models.ForeignKey(Promotion, on_delete=models.CASCADE, related_name='accordion_items')
    order = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Аккордион'
