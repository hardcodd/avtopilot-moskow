from django.contrib import admin
from suit.admin import SortableTabularInline

from . import models


class PaneInline(SortableTabularInline):
    model = models.Pane
    extra = 0
    suit_classes = 'suit-tab suit-tab-panes'


class AccordionInline(SortableTabularInline):
    model = models.Accordion
    extra = 0
    suit_classes = 'suit-tab suit-tab-accordion'


@admin.register(models.Vacations)
class VacationsAdmin(admin.ModelAdmin):
    inlines = [PaneInline, AccordionInline]
    view_on_site = True
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('title', 'slug', 'image', 'content', 'content_middle')
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-panes'),
            'fields': ()
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-accordion'),
            'fields': ()
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-seo'),
            'fields': ('seo_title', 'meta_description', 'meta_keywords', 'meta_image')
        })
    )

    suit_form_tabs = (
        ('general', 'Основное'),
        ('panes', 'Панели'),
        ('accordion', 'Аккордион'),
        ('seo', 'SEO'),
    )
