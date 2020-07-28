from django.contrib import admin
from suit.admin import SortableModelAdmin, SortableTabularInline, SortableStackedInline

from page.forms import HelpForm, HelpItemForm, TabItemForm, TabSectionForm, AboutForm
from . import models


class HomeAboutInline(SortableTabularInline):
    model = models.HomeAbout
    sortable = 'order'
    suit_classes = 'suit-tab suit-tab-about'
    extra = 0


class HomeWorkInline(SortableTabularInline):
    model = models.HomeWork
    sortable = 'order'
    suit_classes = 'suit-tab suit-tab-work'
    extra = 0


@admin.register(models.Home)
class HomeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [HomeAboutInline, HomeWorkInline]
    view_on_site = True

    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('slug', 'title', 'caption', 'header_slider')
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-about'),
            'fields': ()
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-work'),
            'fields': ()
        }),
    )

    suit_form_tabs = (
        ('general', 'Основное'),
        ('about', 'О компании'),
        ('work', 'Как мы работаем')
    )


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    view_on_site = True

    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('title', 'slug')
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


@admin.register(models.Partner)
class PartnerAdmin(SortableModelAdmin):
    list_display = ('title', 'section')
    list_filter = ('section',)
    view_on_site = True

    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('section', 'parent', 'tab_title', 'title')
        }),
        ('Описание', {
            'classes': ('suit-tab', 'suit-tab-description'),
            'fields': ('description',)
        }),
        ('Информация', {
            'classes': ('suit-tab', 'suit-tab-info'),
            'fields': ('info',)
        }),
        ('Карта', {
            'classes': ('suit-tab', 'suit-tab-map'),
            'fields': ('map',)
        })
    )

    suit_form_tabs = (
        ('general', 'Основное'),
        ('description', 'Описание'),
        ('info', 'Информация'),
        ('map', 'Карта'),
    )


class HelpItemInline(SortableStackedInline):
    model = models.HelpItem
    form = HelpItemForm
    sortable = 'order'
    suit_classes = 'suit-tab suit-tab-sections'
    extra = 0


@admin.register(models.Help)
class HelpAdmin(SortableModelAdmin):
    list_display = ('title', 'slug', 'published')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('published',)
    inlines = [HelpItemInline]
    form = HelpForm
    view_on_site = True

    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('published', 'title', 'slug', 'content')
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-seo'),
            'fields': ('seo_title', 'meta_description', 'meta_keywords', 'meta_image')
        })
    )

    suit_form_tabs = (
        ('general', 'Основное'),
        ('sections', 'Разделы'),
        ('seo', 'СЕО'),
    )


class TabSectionInline(SortableStackedInline):
    model = models.TabSection
    form = TabSectionForm
    sortable = 'order'
    extra = 0


@admin.register(models.TabItem)
class TabItemAdmin(SortableModelAdmin):
    form = TabItemForm
    sortable = 'order'
    inlines = [TabSectionInline]
    list_filter = ('parent',)
    search_fields = ('parent', 'title')


@admin.register(models.Info)
class InfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'published')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('published',)
    # form = HelpForm
    view_on_site = True

    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('published', 'title', 'slug', 'content', 'content_bottom')
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


@admin.register(models.StaffMember)
class StaffMemberAdmin(SortableModelAdmin):
    list_display = ('title', 'slug', 'dept', 'position', 'published')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('published',)
    list_filter = ('published', 'dept', 'position')
    sortable_by = 'order'
    # form = HelpForm
    view_on_site = True

    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('published', 'contact_form', 'title', 'slug', 'dept', 'position', 'image', 'video', 'content')
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


@admin.register(models.PortfolioCategory)
class PortfolioCategoryAdmin(SortableModelAdmin):
    list_display = [field.name for field in models.PortfolioCategory._meta.fields]
    prepopulated_fields = {'slug': ('title',)}
    list_display_links = ('id', 'title', 'slug')


@admin.register(models.Work)
class WorkAdmin(SortableModelAdmin):
    pass


@admin.register(models.Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('published', 'title', 'slug', 'content')
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


@admin.register(models.Depd)
class DeptAdmin(SortableModelAdmin):
    pass


class OurOfferInline(SortableStackedInline):
    model = models.OurOffer
    suit_classes = 'suit-tab suit-tab-offers'
    ordering = 'order'
    extra = 0


@admin.register(models.About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'published')
    list_display_links = ('id', 'title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('published',)
    inlines = [OurOfferInline]
    form = AboutForm
    view_on_site = True
    filter_horizontal = ('cases',)

    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('published', 'title', 'slug', 'slider', 'content')
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-offers'),
            'fields': ()
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-become-partner'),
            'fields': ('become_partner',)
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-cases'),
            'fields': ('cases',)
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-content-bottom'),
            'fields': ('content_bottom',)
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-seo'),
            'fields': ('seo_title', 'meta_description', 'meta_keywords', 'meta_image')
        })
    )

    suit_form_tabs = (
        ('general', 'Основное'),
        ('offers', 'Мы предлагаем'),
        ('become-partner', 'Стать партнёром'),
        ('cases', 'Всегда есть чехлы для'),
        ('content-bottom', 'Контент внизу'),
        ('seo', 'СЕО'),
    )
