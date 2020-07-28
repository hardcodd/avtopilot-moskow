from django.db import models
from django.urls import reverse


class LandingPage(models.Model):
	title = models.CharField(max_length=255, verbose_name='Заголовок')
	slug = models.SlugField(verbose_name='Слаг', max_length=255, unique=True)
	theme_color = models.CharField(max_length=255, verbose_name='Цвет браузера на мобилках', default="#7f00ff")
	# Scroll Top Button
	show = models.BooleanField(verbose_name='Отображать кнопку "Наверх"', default=True)
	background = models.CharField(max_length=255, verbose_name='Background', default="linear-gradient(90deg, #7f00ff 0%, #00a3ff 100%)")
	color = models.CharField(max_length=255, verbose_name='Color', default='#fff')
	bottom = models.PositiveSmallIntegerField(verbose_name='Bottom Position', default=10, blank=True, null=True)
	right = models.PositiveSmallIntegerField(verbose_name='Right Position', default=10, blank=True, null=True)
	left = models.PositiveSmallIntegerField(verbose_name='Left Position', blank=True, null=True)
	# SEO
	seo_title = models.CharField(verbose_name='Сео заголовок', max_length=255, blank=True, null=True)
	keywords = models.CharField(verbose_name='Кючевые слова', max_length=255, blank=True, null=True)
	meta_description = models.CharField(verbose_name='Мета описание', max_length=255, blank=True, null=True)
	og_title = models.CharField(verbose_name='Заголовок для соц. сетей', max_length=255, blank=True, null=True)
	og_description = models.CharField(verbose_name='Описание для соц. сетей', max_length=255, blank=True, null=True)
	og_image = models.ImageField(verbose_name='Изображение для соц. сетей', blank=True, null=True)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = 'Landing Page'
		verbose_name_plural = 'Landing Pages'

	def get_absolute_url(self):
			return reverse("lp:lp", kwargs={"slug": self.slug})


class Header(models.Model):
	title = models.CharField(max_length=255, verbose_name='Заголовок', default='Header', help_text='Только для администратора')
	json = models.TextField(verbose_name='JSON Контент', default='')
	parent = models.ForeignKey(LandingPage, on_delete=models.CASCADE, related_name='headers')

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = 'Header'
		verbose_name_plural = 'Headers'


class Section(models.Model):
	title = models.CharField(max_length=255, verbose_name='Заголовок', help_text='Только для администратора')
	order = models.PositiveIntegerField(default=0, db_index=True)
	json = models.TextField(verbose_name='JSON Контент', default='')
	parent = models.ForeignKey(LandingPage, on_delete=models.CASCADE, related_name='sections')

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = 'Section'
		verbose_name_plural = 'Sections'
		ordering = ['order']


class Footer(models.Model):
	title = models.CharField(max_length=255, verbose_name='Заголовок', default='Footer', help_text='Только для администратора')
	json = models.TextField(verbose_name='JSON Контент', default='')
	parent = models.ForeignKey(LandingPage, on_delete=models.CASCADE, related_name='footers')

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = 'Footer'
		verbose_name_plural = 'Footers'
