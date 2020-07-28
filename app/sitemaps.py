from django.contrib.sitemaps import Sitemap
from django.db.models import Q

from catalog.models import Case, UniversalProduct
from page.models import Contact, Home, Help, Info, Portfolio, About
from vacations.models import Vacations


class CasesSitemap(Sitemap):

    def items(self):
        return Case.objects.filter(status='PUBLIC').order_by('-id')

    @staticmethod
    def lastmod(obj):
        return obj.created


class ProductsSitemap(Sitemap):

    def items(self):
        return UniversalProduct.objects.filter(status='PUBLIC').order_by('-id')

    @staticmethod
    def lastmod(obj):
        return obj.created


class ContactsSitemap(Sitemap):

    def items(self):
        return Contact.objects.filter(slug='contacts')


class HomeSitemap(Sitemap):

    def items(self):
        return Home.objects.all()


class HelpSitemap(Sitemap):

    def items(self):
        return Help.objects.filter(published=True)


class InfoSitemap(Sitemap):

    def items(self):
        exclude_pages = [
            'politika-konfidencialnosti', 'publichnaya-oferta',
            'spasibo-za-zakaz'
        ]
        return Info.objects.filter(~Q(slug__in=exclude_pages), published=True)


class PortfolioSitemap(Sitemap):

    def items(self):
        return Portfolio.objects.filter(published=True)


class AboutSitemap(Sitemap):

    def items(self):
        return About.objects.filter(published=True)


class VacationsSitemap(Sitemap):

    def items(self):
        return Vacations.objects.all()
