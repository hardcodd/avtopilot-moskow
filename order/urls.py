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

from . import views

urlpatterns = [
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
    path('get_products_in_cart/', views.products_in_cart, name='get_products_in_cart'),
    path('get_delivery_methods/', views.ajax_get_delivery_methods, name='ajax_get_delivery_methods'),
    path('yandex_payment/<int:pk>/<uuid:_uuid>/', views.yandex_payment, name='yandex_payment'),
    path('order/', views.order, name='ordering'),
    path('order_sew/', views.order_sew, name='ordering_sew'),
]
