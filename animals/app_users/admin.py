from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from .models import User
from django.contrib.auth.admin import UserAdmin
"""
Registers the User model in the admin panel.
"""


@admin.action(description='Mark as guest')
def mark_as_guest(model_admin: admin.ModelAdmin, request: HttpRequest, query_set: QuerySet):
    query_set.update(is_guest=True)


@admin.action(description='Unmark as guest')
def unmark_as_guest(model_admin: admin.ModelAdmin, request: HttpRequest, query_set: QuerySet):
    query_set.update(is_guest=False)


@admin.register(User)
class UserAdmin(UserAdmin):
    model = User
    list_display = 'id', 'username', 'shelter', 'is_guest'
    ordering = 'pk',
    actions = mark_as_guest, unmark_as_guest,
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", 'shelter'),
            },
        ),
    )
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('shelter', 'is_guest', 'asked_for_upgrade',)
            }
        )
    )

