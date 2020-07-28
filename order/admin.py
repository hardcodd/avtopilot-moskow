from adminsortable.admin import SortableAdmin
from django.contrib import admin
from . import models


@admin.register(models.ProductInCart)
class ProductInCartAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.ProductInCart._meta.fields]


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'full_name', 'email', 'current_status', 'payment_status', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('pk', 'full_name', 'email', 'timestamp')


@admin.register(models.DeliveryMethod)
class DeliveryMethodAdmin(SortableAdmin):
    list_display = ('title', 'price')
