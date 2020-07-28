from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Menu(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=255)
    slug = models.SlugField(verbose_name='Слаг', unique=True)
    order = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def get_items(self):
        items = MenuItem.objects.filter(menu=self).order_by('order')
        return items


class MenuItem(MPTTModel):
    title = models.CharField(verbose_name='Заголовок', max_length=255)
    url = models.CharField(verbose_name='Ссылка', max_length=255, default='#')
    blank = models.BooleanField(verbose_name='В новой вкладке', default=False)
    parent = TreeForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='children')
    css_class = models.CharField(verbose_name='CSS Класс', max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return self.title
