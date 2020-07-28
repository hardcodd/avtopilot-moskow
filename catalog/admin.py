from adminsortable.admin import SortableAdmin
from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from suit.admin import SortableTabularInline, SortableModelAdmin, SortableStackedInline

from catalog.forms import MaterialForm, CaseForm
from . import models


@admin.register(models.Model)
class ModelAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'title', 'make')
    list_display_links = ('id', 'title')
    list_editable = ('make',)
    search_fields = ('title',)
    list_filter = ('make',)


@admin.register(models.Make)
class MakeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug')
    list_editable = ('slug',)
    list_filter = ('model',)
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    view_on_site = True
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'image', 'video', 'title_description', 'description')
        }),
        ('СЕО', {
            'fields': ('seo_title', 'meta_description', 'meta_keywords', 'meta_image')
        })
    )


class ImageInline(SortableTabularInline):
    model = models.Image
    sortable = 'order'
    suit_classes = 'suit-tab suit-tab-media'
    extra = 0


class MaterialInline(SortableStackedInline):
    model = models.Material
    sortable = 'order'
    suit_classes = 'suit-tab suit-tab-general'
    form = MaterialForm
    extra = 0
    filter_horizontal = ('colors',)


@admin.register(models.Reviews)
class TabReviewsAdmin(SortableModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = ({'slug': ('title',)})
    view_on_site = True


@admin.register(models.QnA)
class QnAAdmin(SortableModelAdmin):
    pass


@admin.register(models.Case)
class CaseAdmin(SortableModelAdmin):
    list_display = ('title', 'slug', 'created', 'updated', 'status')
    # list_editable = ('status',)
    list_filter = ('model__make', 'model', 'created', 'updated', 'status')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [MaterialInline, ImageInline]
    view_on_site = True
    save_as = True
    form = CaseForm
    list_per_page = 100
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('status', 'title', 'slug', 'install_price', 'code', 'model', 'weight', 'guarantee')
        }),
        ('Медиа', {
            'classes': ('suit-tab', 'suit-tab-media'),
            'fields': ('image', 'video')
        }),
        ('Табы', {
            'classes': ('suit-tab', 'suit-tab-tabs'),
            'fields': ('description', 'stock', 'install', 'tab_reviews', 'qna', 'accessories')
        }),
        ('СЕО', {
            'classes': ('suit-tab', 'suit-tab-seo'),
            'fields': ('seo_title', 'meta_description', 'meta_keywords', 'meta_image')
        })
    )
    suit_form_tabs = (
        ('general', 'Основное'),
        ('media', 'Медиа'),
        ('tabs', 'Табы'),
        ('seo', 'СЕО'),
    )

    filter_horizontal = ('tab_reviews', 'qna', 'accessories')


@admin.register(models.Guarantee)
class GuaranteeAdmin(admin.ModelAdmin):
    list_display = ('title', 'period')
    prepopulated_fields = {'slug': ('title', 'period')}
    view_on_site = True

    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('title', 'period', 'slug', 'content')
        }),
        ('СЕО', {
            'classes': ('suit-tab', 'suit-tab-seo'),
            'fields': ('seo_title', 'meta_description', 'meta_keywords', 'meta_image')
        })
    )
    suit_form_tabs = (
        ('general', 'Основное'),
        ('seo', 'СЕО'),
    )


@admin.register(models.Color)
class ColorAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_filter = ('material_name',)
    fieldsets = (
        (None, {
            'fields': ('material_name', 'code', 'color_name', 'image', 'big_image', 'video')
        }),
    )


class UniversalImageInline(SortableTabularInline):
    model = models.UniversalImage
    sortable = 'order'
    suit_classes = 'suit-tab suit-tab-media'
    extra = 1


class UniversalSizeInline(SortableTabularInline):
    model = models.UniversalSize
    sortable = 'order'
    suit_classes = 'suit-tab suit-tab-general'
    extra = 0


class UniversalColorInline(SortableTabularInline):
    model = models.UniversalColor
    sortable = 'order'
    suit_classes = 'suit-tab suit-tab-general'
    extra = 0


@admin.register(models.UniversalProduct)
class UniversalProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'price', 'product_type', 'created', 'updated')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('product_type', 'created', 'updated')
    filter_horizontal = ('tab_reviews', 'qna', 'accessories')
    view_on_site = True
    inlines = [UniversalColorInline, UniversalImageInline, UniversalSizeInline]
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('status', 'product_type', 'title', 'slug', 'category', 'weight', 'info', 'guarantee')
        }),
        ('Медиа', {
            'classes': ('suit-tab', 'suit-tab-media'),
            'fields': ('image', 'video')
        }),
        ('Табы', {
            'classes': ('suit-tab', 'suit-tab-tabs'),
            'fields': ('description', 'install', 'tab_reviews', 'qna', 'accessories')
        }),
        ('СЕО', {
            'classes': ('suit-tab', 'suit-tab-seo'),
            'fields': ('seo_title', 'meta_description', 'meta_keywords', 'meta_image')
        })
    )
    suit_form_tabs = (
        ('general', 'Основное'),
        ('media', 'Медиа'),
        ('tabs', 'Табы'),
        ('seo', 'СЕО'),
    )


@admin.register(models.UniversalCategory)
class UniversalCategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'products_type')
    search_fields = ('title',)
    list_display_links = ('title',)
    list_filter = ('products_type',)


@admin.register(models.CatalogPage)
class CatalogPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'seo_title', 'meta_keywords', 'meta_description')
    list_editable = ('seo_title', 'meta_keywords', 'meta_description')
    prepopulated_fields = {'slug': ('title',)}
    view_on_site = True

    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('model', 'title', 'slug', 'video', 'title_description', 'description')
        }),
        ('СЕО', {
            'classes': ('suit-tab', 'suit-tab-seo'),
            'fields': ('seo_title', 'meta_description', 'meta_keywords', 'meta_image')
        })
    )
    suit_form_tabs = (
        ('general', 'Основное'),
        ('seo', 'СЕО'),
    )


@admin.register(models.Install)
class InstallAdmin(admin.ModelAdmin):
    list_display = ('title',)

    fieldsets = (
        (None, {
            'fields': ('title', 'content')
        }),
    )


@admin.register(models.Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('title',)

    fieldsets = (
        (None, {
            'fields': ('title', 'content')
        }),
    )


@admin.register(models.PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'percent')
