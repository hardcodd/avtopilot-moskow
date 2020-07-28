"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from app.forms_handler import forms_handler
from . import views

urlpatterns = [
    # TURBO
    path('cases_turbo/', views.cases_turbo, name='cases_turbo'),
    # END TURBO

    path('order/', views.order, name='order'),
    path('cart/', views.cart_detail, name='cart'),
    path('load-more-products/', views.catalog_page_load_more, name='catalog_page_load_more'),
    path('check_promo_code/', views.check_promo_code, name='check_promo_code'),
    path('filter-products/', views.catalog_page_filter, name='catalog_page_filter'),
    path('<slug:slug>/', views.catalog_page, name='catalog_page'),
    path('category/<slug:slug>/', views.products_category, name='products_category'),
    path('make/<slug:slug>/', views.make, name='make'),
    path('case/<slug:slug>/', views.case_detail, name='case_detail'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('review/<slug:slug>/', views.review_detail, name='review_detail'),
    path('guarantee/<slug:slug>/', views.guarantee, name='guarantee'),
    path('forms_handler', forms_handler, name='forms_handler'),
    path('', views.home, name='home')
]
