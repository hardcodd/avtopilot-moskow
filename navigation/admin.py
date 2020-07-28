from django.contrib import admin
from suit.admin import SortableTabularInline

from navigation.models import Menu, MenuItem


class MenuItemInline(SortableTabularInline):
    model = MenuItem
    sortable = 'order'
    extra = 0


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug')
    list_display_links = list_display
    prepopulated_fields = {'slug': ('title',)}
    inlines = [MenuItemInline]
