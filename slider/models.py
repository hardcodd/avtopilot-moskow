from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField

from app.utils import video_url


class Slider(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(verbose_name='Слаг')

    class Meta:
        verbose_name = 'Слайдер'
        verbose_name_plural = 'Слайдер'

    def __str__(self):
        return self.title

    @property
    def get_slides(self):
        return self.slides.all().order_by('order')

    @property
    def slides_count(self):
        return self.slides.count()
    slides_count.fget.short_description = 'Количество слайдов'


class Slide(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    video = models.URLField(verbose_name='Ссылка на видео', blank=True)
    url = models.URLField(verbose_name='Ссылка', blank=True)
    blank = models.BooleanField(verbose_name='В новой вкладке', default=False)
    image = ThumbnailerImageField(verbose_name='Изображение', blank=True)
    parent = models.ForeignKey(Slider, on_delete=models.CASCADE, related_name='slides')
    order = models.PositiveIntegerField(blank=True, null=True)

    @property
    def video_url(self):
        return video_url(self.video)
