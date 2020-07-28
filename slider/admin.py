from django.contrib import admin
from suit.admin import SortableTabularInline

from . import models


class SlideInline(SortableTabularInline):
    model = models.Slide
    sortable = 'order'
    extra = 0


@admin.register(models.Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'slides_count')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [SlideInline]
