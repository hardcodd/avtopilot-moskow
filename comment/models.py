from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from easy_thumbnails.fields import ThumbnailerImageField

from app.utils import fn
from app.my_storage import MyStorage as Fs


class ReviewManager(models.Manager):
    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(ReviewManager, self).filter(content_type=content_type, object_id=obj_id,
                                               publish_date__lte=timezone.now())
        return qs


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    rating = models.PositiveIntegerField(blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    publish_date = models.DateTimeField(auto_now_add=False, default=timezone.now, blank=True, null=True)

    objects = ReviewManager()

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы на товары и услуги'

    def __str__(self):
        return self.user.full_name


class MainReviewSection(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(verbose_name='Слаг', unique=True)
    order = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    def __str__(self):
        return self.title

    @property
    def get_reviews(self):
        return self.mainreview_set.filter(published=True).order_by('?')[:10]


class MainReview(models.Model):
    published = models.BooleanField(verbose_name='Опубликовано', default=False)
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='E-mail')
    phone = models.CharField(max_length=100, verbose_name='Телефон')
    image = ThumbnailerImageField(verbose_name='Изображение', storage=Fs(), upload_to=fn, blank=True, null=True)
    video = models.URLField(max_length=255, verbose_name='Ссылка на видео', blank=True, null=True)
    content = RichTextField(verbose_name='Комментарий', config_name='special', blank=True, null=True)
    section = models.ForeignKey(MainReviewSection, verbose_name='Раздел', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Общие отзывы'

    def __str__(self):
        return self.name
