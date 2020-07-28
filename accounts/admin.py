from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db import models
from django.forms import SelectMultiple

from accounts.models import UserGroup
from .forms import UserAdminCreationForm, UserAdminChangeForm
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'is_active')
    list_filter = ('is_superuser', 'is_staff')
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-account'),
            'fields': ('email', 'password')
        }),
        ('Персональная информация', {
            'classes': ('suit-tab', 'suit-tab-personal-info'),
            'fields': ('first_name', 'last_name', 'middle_name', 'born', 'gender', 'avatar')
        }),
        ('Контактные данные', {
            'classes': ('suit-tab', 'suit-tab-contacts'),
            'fields': ('phone',)
        }),
        ('Адрес', {
            'classes': ('suit-tab', 'suit-tab-address'),
            'fields': ('country', 'city', 'street', 'house_num', 'housing_num', 'flat_num')
        }),
        ('Права доступа', {
            'classes': ('suit-tab', 'suit-tab-permissions'),
            'fields': ('is_superuser', 'is_staff', 'is_active', 'groups')
        }),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

    suit_form_tabs = (
        ('account', 'Аккаунт'),
        ('personal-info', 'Персональная информация'),
        ('contacts', 'Контактные данные'),
        ('address', 'Адрес'),
        ('permissions', 'Права доступа'),
    )


class UserGroupAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': forms.SelectMultiple(attrs={
            'class': 'input-xxlarge',
            'size': '30'
        })}
    }
    filter_horizontal = ('permissions',)


admin.site.register(User, UserAdmin)
admin.site.register(UserGroup, UserGroupAdmin)

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)
