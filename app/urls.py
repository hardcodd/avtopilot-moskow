from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib.sitemaps.views import sitemap

from app.google_recaptcha import check
from app.sitemaps import (
    CasesSitemap, ProductsSitemap,
    ContactsSitemap, HomeSitemap, HelpSitemap, InfoSitemap,
    PortfolioSitemap, AboutSitemap, VacationsSitemap
)

sitemaps = {
    'cases': CasesSitemap,
    'products': ProductsSitemap,
    'contacts': ContactsSitemap,
    'home': HomeSitemap,
    'help': HelpSitemap,
    'info': InfoSitemap,
    'portfolio': PortfolioSitemap,
    'about': AboutSitemap,
    'vacations': VacationsSitemap
}

urlpatterns = [
    # path('jet/', include('jet.urls', 'jet')),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', include('robots.urls')),
    path('builder/', include('builder.urls')),
    path('aristarx/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('vacations/', include('vacations.urls')),
    path('promotion/', include('promotion.urls')),
    path('reviews/', include('comment.urls')),
    path('account/', include('accounts.urls')),
    path('order/', include('order.urls')),
    path('page/', include('page.urls')),
    path('search/', include('search.urls')),
    path('lp/', include('lp.urls')),
    path('google-recaptcha/', check),

    path('filer/', include('filer.urls')),

    path('fail-payment/', TemplateView.as_view(template_name='fail.html'), name='payment_fail'),
    path('success-payment/', TemplateView.as_view(template_name='success.html'), name='payment_success'),
    path('yandex-money/', include('yandex_money.urls')),

    path('', include('catalog.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
