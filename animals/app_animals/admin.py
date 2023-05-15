from django.contrib import admin
from .models import Shelter, Animal


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'shelter'


class AnimalInline(admin.TabularInline):
    model = Animal


@admin.register(Shelter)
class ShelterAdmin(admin.ModelAdmin):
    list_display = 'id', 'title'
    inlines = [AnimalInline]
