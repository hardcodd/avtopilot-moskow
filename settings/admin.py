from django.contrib import admin
from suit.admin import SortableTabularInline, SortableStackedInline

from settings.models import General, Moderator, Social, BlogWidget


class ModeratorInline(SortableTabularInline):
    model = Moderator
    suit_classes = 'suit-tab suit-tab-moderators'
    extra = 0


class BlogWidgetInline(SortableTabularInline):
    model = BlogWidget
    suit_classes = 'suit-tab suit-tab-blog'
    extra = 0


class SocialInline(SortableStackedInline):
    model = Social
    suit_classes = 'suit-tab suit-tab-contacts'
    extra = 0


@admin.register(General)
class GeneralAdmin(admin.ModelAdmin):
    filter_horizontal = ('accessories',)
    inlines = [ModeratorInline, SocialInline, BlogWidgetInline]
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-seo'),
            'fields': (
                'title',
                'title_part',
                'divider',
                'keywords',
                'description',
                'meta_image',
            )
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-contacts'),
            'fields': (
                'phone_free',
                'phone',
                'email',
                'city',
                'address',
                'zip',
                'work_time',
                'work_time_header',
                'map'
            )
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-accessories'),
            'fields': ('accessories',)
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-blog'),
            'fields': ()
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-moderators'),
            'fields': ()
        })
    )

    suit_form_tabs = (
        ('seo', 'СЕО'),
        ('accessories', 'Аксессуары'),
        ('contacts', 'Контакты'),
        ('blog', 'Блог'),
        ('moderators', 'Модераторы'),
    )
