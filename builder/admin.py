from adminsortable.admin import NonSortableParentAdmin, SortableTabularInline, SortableAdmin
from django.contrib import admin

from builder.models import \
    CaseBuilder, Base, Rear, Type, \
    Material, Color, Seam, SeamColor, \
    MateBuilder, MateColor, MateSeamColor


@admin.register(Base)
class BaseAdmin(SortableAdmin):
    pass


@admin.register(Rear)
class RearAdmin(SortableAdmin):
    pass


class SeamColorAdminInline(SortableTabularInline):
    model = SeamColor
    fields = ('title', 'image', 'hex')
    ordering = ['order']
    extra = 0


class MateSeamColorAdminInline(SortableTabularInline):
    model = MateSeamColor
    fields = ('title', 'hex')
    ordering = ['order']
    extra = 0


@admin.register(Seam)
class SeamAdmin(SortableAdmin):
    inlines = [SeamColorAdminInline]


class TypeAdminInline(SortableTabularInline):
    model = Type
    ordering = ['order']
    extra = 0
    fields = ('title',)


@admin.register(CaseBuilder)
class CaseBuilderAdmin(SortableAdmin):
    inlines = [TypeAdminInline]


class ColorAdminInline(SortableTabularInline):
    model = Color
    fields = ('title', 'image', 'hex')
    ordering = ['order']
    extra = 0


class MateColorAdminInline(SortableTabularInline):
    model = MateColor
    fields = ('title', 'image')
    ordering = ['order']
    extra = 0


@admin.register(Material)
class MaterialAdmin(SortableAdmin):
    list_display = ('title', 'parent', 'price')
    list_filter = ('parent',)
    inlines = [ColorAdminInline]


@admin.register(MateBuilder)
class MateBuilderAdmin(SortableAdmin):
    inlines = [MateColorAdminInline, MateSeamColorAdminInline]
