from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import Shelter, Animal

"""
Registers Animal and Shelter models in the admin panel.
"""


@admin.action(description='Mark archived')
def mark_archived(model_admin: admin.ModelAdmin, request: HttpRequest, query_set: QuerySet):
    query_set.update(is_archived=True)


@admin.action(description='Unmark archived')
def unmark_archived(model_admin: admin.ModelAdmin, request: HttpRequest, query_set: QuerySet):
    query_set.update(is_archived=False)


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'shelter', 'is_archived',
    actions = [mark_archived, unmark_archived]


class AnimalInline(admin.TabularInline):
    model = Animal


@admin.register(Shelter)
class ShelterAdmin(admin.ModelAdmin):
    list_display = 'id', 'title'
    inlines = [AnimalInline]
