from django.contrib import admin
from suit.admin import SortableTabularInline, SortableModelAdmin, SortableStackedInline
from . import models


class SlideInline(SortableTabularInline):
    model = models.Slide
    suit_classes = 'suit-tab suit-tab-slider'
    extra = 0


class AccordionInline(SortableStackedInline):
    model = models.Accordion
    suit_classes = 'suit-tab suit-tab-accordion'
    extra = 0


@admin.register(models.Category)
class CategoryAdmin(SortableModelAdmin):
    list_display = ('title', 'widget_title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(models.Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'time_end', 'published')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('category', 'published', 'time_end')
    inlines = [SlideInline, AccordionInline]

    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('published', 'title', 'slug', 'category', 'image', 'video', 'price', 'discounted', 'time_end')
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-slider'),
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
        ('slider', 'Слайдер'),
        ('accordion', 'Аккордион'),
        ('seo', 'СЕО'),
    )


@admin.register(models.PromotionPage)
class PromotionPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'published')
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('published', 'title', 'slug')
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-seo'),
            'fields': ('seo_title', 'meta_description', 'meta_keywords', 'meta_image')
        })
    )

    suit_form_tabs = (
        ('general', 'Основное'),
        ('seo', 'СЕО'),
    )
