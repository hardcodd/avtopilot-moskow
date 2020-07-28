from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.db.models import TextField
from django_ace import AceWidget

from . import models


class HeaderInline(admin.StackedInline):
	model = models.Header
	extra = 1
	max_num = 1
	min_num = 1
	formfield_overrides = {
			TextField: {'widget': AceWidget(mode='json', theme='dracula', wordwrap=True, width='100%', height='600px', usesofttabs=False, tabsize=2)},
	}
	class Media:
		css = {
				'all': ['lp/admin/css/admin.css']
		}


class SectionInline(SortableInlineAdminMixin, admin.StackedInline):
	model = models.Section
	extra = 0
	formfield_overrides = {
			TextField: {'widget': AceWidget(mode='json', theme='dracula', wordwrap=True, width='100%', height='600px', usesofttabs=False, tabsize=2)},
	}
	class Media:
		css = {
				'all': ['lp/admin/css/admin.css']
		}
		js = ('lp/admin/js/admin.js',)


class FooterInline(admin.StackedInline):
	model = models.Footer
	extra = 1
	max_num = 1
	min_num = 1
	formfield_overrides = {
			TextField: {'widget': AceWidget(mode='json', theme='dracula', wordwrap=True, width='100%', height='600px', usesofttabs=False, tabsize=2)},
	}
	class Media:
		css = {
				'all': ['lp/admin/css/admin.css']
		}


@admin.register(models.LandingPage)
class LandingPageAdmin(admin.ModelAdmin):
	inlines = (HeaderInline, SectionInline, FooterInline)
	view_on_site = True
	fieldsets = (
			(None, {
					"fields": (
							'title', 'slug', 'theme_color'
					),
			}),
			('Кнопка "Наверх"', {
					"fields": (
							'show', 'background', 'color', 'bottom', 'right', 'left'
					),
			}),
			('СЕО', {
					"fields": (
							'seo_title', 'keywords', 'meta_description', 'og_title', 'og_description', 'og_image'
					),
			}),
	)
