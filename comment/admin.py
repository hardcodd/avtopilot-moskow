from django.contrib import admin
from suit.admin import SortableModelAdmin

from . import models

admin.site.register(models.Review)


@admin.register(models.MainReview)
class MainReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email', 'section', 'published')
    list_filter = ('published', 'section',)
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'phone', 'email')


@admin.register(models.MainReviewSection)
class MainReviewSectionAdmin(SortableModelAdmin):
    list_display = ('title', 'slug', 'order')
    prepopulated_fields = {'slug': ('title',)}
