from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.urls import reverse
from easy_thumbnails.fields import ThumbnailerImageField

from app.my_storage import MyStorage as Fs
from app.utils import fn, video_url, video_image
from django.db import models

from catalog.models import Case, Make
from comment.utils import get_reviews
from slider.models import Slider


class Contact(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(verbose_name='Слаг', unique=True)
    order = models.PositiveIntegerField(blank=True, null=True)
    # SEO
    seo_title = models.CharField(max_length=255, verbose_name='СЕО Заголовок', blank=True, null=True)
    meta_description = models.CharField(max_length=260, verbose_name='Мета описание', blank=True, null=True)
    meta_keywords = models.CharField(max_length=160, verbose_name='Ключевые слова', blank=True, null=True)
    meta_image = ThumbnailerImageField(verbose_name='Изображение для соц. сетей', blank=True, null=True)

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Контакты, Команда, Отзывы'

    def __str__(self):
        return self.title

    def get_edit_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

    def get_absolute_url(self):
        return reverse('contacts')

class Partner(models.Model):
    CHOICES = (
        ('PARTNERS', 'Наши партнёры в России'),
        ('OTHER_PARTNERS', 'Наши партнёры в других странах'),
        ('INSTALL', 'Где можно установить'),
    )
    section = models.CharField(max_length=255, verbose_name='Раздел', choices=CHOICES)
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    tab_title = models.CharField(max_length=255, verbose_name='Заголовок таба')
    parent = models.ForeignKey(Contact, verbose_name='Родительская', on_delete=models.CASCADE, related_name='partners')
    description = RichTextUploadingField(verbose_name='Описание', blank=True)
    info = RichTextUploadingField(verbose_name='Информация', blank=True)
    map = models.TextField(verbose_name='Карта', blank=True)
    order = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Партнёр'
        verbose_name_plural = 'Партнёры'

    def __str__(self):
        return self.title


class Home(models.Model):
    slug = models.SlugField(verbose_name='Слаг')
    title = models.CharField(max_length=255, verbose_name='Заголовок', blank=True)
    caption = models.CharField(max_length=255, verbose_name='Описание над заголовком', blank=True)
    header_slider = models.ForeignKey(Slider, verbose_name='Слайдер', blank=True, null=True, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Главная'
        verbose_name_plural = 'Главная'

    def __str__(self):
        return 'Главная ID:%s' % (self.id,)

    @property
    def about(self):
        return HomeAbout.objects.filter(parent=self).order_by('order')

    @property
    def work(self):
        return HomeWork.objects.filter(parent=self).order_by('order')

    @staticmethod
    def get_absolute_url():
        from django.urls import reverse
        return reverse('home')

    def get_edit_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))


class HomeAbout(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок', blank=True)
    icon = models.TextField(verbose_name='SVG Иконка', blank=True)
    content = models.TextField(verbose_name='Контент', blank=True)
    parent = models.ForeignKey(Home, verbose_name='Родительская',
                               on_delete=models.CASCADE, related_name='about_items')
    order = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'О компании'


class HomeWork(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок', blank=True)
    icon = models.TextField(verbose_name='SVG Иконка', blank=True)
    content = models.TextField(verbose_name='Контент', blank=True)
    parent = models.ForeignKey(Home, verbose_name='Родительская',
                               on_delete=models.CASCADE, related_name='work_items')
    order = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Как мы работаем'


class Help(models.Model):
    published = models.BooleanField(verbose_name='Опубликовано', default=False)
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(verbose_name='Слаг', unique=True)
    content = RichTextUploadingField(verbose_name='Контент', blank=True)
    order = models.PositiveIntegerField(blank=True, null=True)
    # SEO
    seo_title = models.CharField(max_length=255, verbose_name='СЕО Заголовок', blank=True, null=True)
    meta_description = models.CharField(max_length=260, verbose_name='Мета описание', blank=True, null=True)
    meta_keywords = models.CharField(max_length=160, verbose_name='Ключевые слова', blank=True, null=True)
    meta_image = ThumbnailerImageField(verbose_name='Изображение для соц. сетей', blank=True, null=True)

    class Meta:
        verbose_name = 'Помощь'
        verbose_name_plural = 'Помощь'

    def __str__(self):
        return self.title

    @property
    def items(self):
        return HelpItem.objects.filter(parent=self).order_by('order')

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('help', args=[str(self.slug)])

    def get_edit_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))


class HelpItem(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок', blank=True)
    content = RichTextUploadingField(verbose_name='Контент', blank=True)
    parent = models.ForeignKey(Help, on_delete=models.CASCADE, related_name='help_items')
    order = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    def __str__(self):
        return self.title


class Info(models.Model):
    published = models.BooleanField(verbose_name='Опубликовано', default=False)
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(verbose_name='Слаг', unique=True)
    content = RichTextUploadingField(verbose_name='Контент', blank=True)
    content_bottom = RichTextUploadingField(verbose_name='Контент внизу страницы', blank=True)
    order = models.PositiveIntegerField(blank=True, null=True)
    # SEO
    seo_title = models.CharField(max_length=255, verbose_name='СЕО Заголовок', blank=True, null=True)
    meta_description = models.CharField(max_length=260, verbose_name='Мета описание', blank=True, null=True)
    meta_keywords = models.CharField(max_length=160, verbose_name='Ключевые слова', blank=True, null=True)
    meta_image = ThumbnailerImageField(verbose_name='Изображение для соц. сетей', blank=True, null=True)

    class Meta:
        verbose_name = 'Инфо'
        verbose_name_plural = 'Инфо'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('info', args=[str(self.slug)])

    @property
    def tabs(self):
        return TabItem.objects.filter(parent=self).order_by('order')

    def get_edit_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))


class TabItem(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок', blank=True)
    parent = models.ForeignKey(Info, verbose_name='Инфо', on_delete=models.CASCADE, related_name='tab_items')
    order = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Таб'
        verbose_name_plural = 'Инфо-табы'

    def __str__(self):
        return self.title

    @property
    def tab_sections(self):
        return self.tab_section_items.order_by('order')


class TabSection(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок', blank=True)
    content = RichTextUploadingField(verbose_name='Контент', blank=True)
    parent = models.ForeignKey(TabItem, on_delete=models.CASCADE, related_name='tab_section_items')
    order = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    def __str__(self):
        return self.title


class Depd(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    order = models.PositiveIntegerField(blank=True, null=True)

    @property
    def get_members(self):
        return self.staffmember_set.filter(published=True).order_by('order')

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы сотрудников'

    def __str__(self):
        return self.title


class StaffMember(models.Model):
    published = models.BooleanField(verbose_name='Опубликовано', default=False)
    dept = models.ForeignKey(Depd, verbose_name='Отдел', on_delete=models.CASCADE)
    contact_form = models.BooleanField(verbose_name='Контактная форма', default=False)
    title = models.CharField(max_length=255, verbose_name='Имя')
    slug = models.SlugField(verbose_name='Слаг', unique=True)
    position = models.CharField(max_length=255, verbose_name='Должность', blank=True, null=True)
    image = ThumbnailerImageField(verbose_name='Фото (510x595)', blank=True, null=True)
    video = models.URLField(max_length=255, verbose_name='Ссылка на видео', blank=True, null=True)
    content = RichTextUploadingField(verbose_name='Контент', blank=True)
    order = models.PositiveIntegerField(blank=True, null=True)
    # SEO
    seo_title = models.CharField(max_length=255, verbose_name='СЕО Заголовок', blank=True, null=True)
    meta_description = models.CharField(max_length=260, verbose_name='Мета описание', blank=True, null=True)
    meta_keywords = models.CharField(max_length=160, verbose_name='Ключевые слова', blank=True, null=True)
    meta_image = ThumbnailerImageField(verbose_name='Изображение для соц. сетей', blank=True, null=True)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.title

    @property
    def portfolio(self):
        return Work.objects.filter(staff=self).order_by('order')

    @property
    def get_position(self):
        return self.position or self.dept.title

    @property
    def reviews(self):
        return get_reviews(self)

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance).model
        return content_type

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('staff', args=[str(self.slug)])

    def get_edit_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))


class Portfolio(models.Model):
    published = models.BooleanField(verbose_name='Опубликовано', default=False)
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(verbose_name='Слаг', unique=True)
    content = RichTextUploadingField(verbose_name='Контент', blank=True)
    order = models.PositiveIntegerField(blank=True, null=True)
    # SEO
    seo_title = models.CharField(max_length=255, verbose_name='СЕО Заголовок', blank=True, null=True)
    meta_description = models.CharField(max_length=260, verbose_name='Мета описание', blank=True, null=True)
    meta_keywords = models.CharField(max_length=160, verbose_name='Ключевые слова', blank=True, null=True)
    meta_image = ThumbnailerImageField(verbose_name='Изображение для соц. сетей', blank=True, null=True)

    class Meta:
        verbose_name = 'Портфолио'
        verbose_name_plural = 'Портфолио'

    def __str__(self):
        return self.title

    @property
    def portfolio_categories(self):
        return PortfolioCategory.objects.all().order_by('order')

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('portfolio', args=[str(self.slug)])

    def get_edit_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))


class PortfolioCategory(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(verbose_name='Слаг', unique=True)
    order = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории портфолио'

    @property
    def works_video(self):
        return Work.objects.filter(~Q(video=None), category=self).order_by('order')

    @property
    def works_photo(self):
        return Work.objects.filter(~Q(image=''), category=self).order_by('order')


class Work(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    category = models.ForeignKey(PortfolioCategory, verbose_name='Категория', on_delete=models.CASCADE)
    staff = models.ForeignKey(StaffMember, verbose_name='Сотрудник', on_delete=models.CASCADE, blank=True, null=True)
    video = models.URLField(max_length=255, verbose_name='Ссылка на видео', blank=True, null=True)
    image = ThumbnailerImageField(verbose_name='Изображение (800x450)', storage=Fs(), upload_to=fn, blank=True, null=True)
    caption = models.TextField(max_length=255, verbose_name='Описание', blank=True, null=True)
    order = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Работа'
        verbose_name_plural = 'Работы'

    @property
    def get_video_url(self):
        if self.video:
            return video_url(self.video)

    @property
    def get_video_image(self):
        if self.video:
            return video_image(self.video)


class About(models.Model):
    published = models.BooleanField(verbose_name='Опубликовано', default=False)
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(verbose_name='Слаг', unique=True)
    content = RichTextUploadingField(verbose_name='Контент', blank=True)
    become_partner = RichTextUploadingField(verbose_name='Стать партнёром', blank=True)
    cases = models.ManyToManyField(Make, verbose_name='Всегда есть чехлы для',
                                   related_name='cases', blank=True)
    slider = models.ForeignKey(Slider, verbose_name='Слайдер (Наша фабрика)',
                               blank=True, null=True, on_delete=models.CASCADE)
    content_bottom = RichTextUploadingField(verbose_name='Нижний контент', blank=True)
    order = models.PositiveIntegerField(blank=True, null=True)
    # SEO
    seo_title = models.CharField(max_length=255, verbose_name='СЕО Заголовок', blank=True, null=True)
    meta_description = models.CharField(max_length=260, verbose_name='Мета описание', blank=True, null=True)
    meta_keywords = models.CharField(max_length=160, verbose_name='Ключевые слова', blank=True, null=True)
    meta_image = ThumbnailerImageField(verbose_name='Изображение для соц. сетей', blank=True, null=True)

    class Meta:
        verbose_name = 'О компании'
        verbose_name_plural = 'О компании'

    def __str__(self):
        return self.title

    @property
    def get_offers(self):
        return self.offers.all().order_by('order')

    @property
    def get_cases(self):
        return self.cases.all().order_by('title')

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('about', args=[str(self.slug)])

    def get_edit_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))


class OurOffer(models.Model):
    image = ThumbnailerImageField(verbose_name='Фото (510x287)', blank=True, null=True)
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Контент')
    url = models.CharField(max_length=255, verbose_name='Ссылка',
                           help_text='Если сылка на текущий сайт, то URL должен выглядеть так: <code>/path/to/</code>')
    parent = models.ForeignKey(About, on_delete=models.CASCADE, related_name='offers')
    order = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Предложение'
        verbose_name_plural = ''

    def __str__(self):
        return self.title
