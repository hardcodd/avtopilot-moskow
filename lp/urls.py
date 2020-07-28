from django.urls import path
from lp import views


app_name = 'lp'


urlpatterns = [
	path('bx24/', views.bx24, name='bx24'),
	path('<slug:slug>/', views.lp, name='lp')
]
