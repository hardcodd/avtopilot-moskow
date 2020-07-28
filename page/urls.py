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
    path('contacts/', views.contacts, name='contacts'),
    path('team/', views.team, name='team'),
    path('reviews/', views.reviews, name='reviews'),
    path('help/<slug:slug>/', views.help_page, name='help'),
    path('info/<slug:slug>/', views.info_page, name='info'),
    path('staff/<slug:slug>/', views.staff_page, name='staff'),
    path('portfolio/<slug:slug>/', views.portfolio_page, name='portfolio'),
    path('about/<slug:slug>/', views.about_page, name='about'),
]
