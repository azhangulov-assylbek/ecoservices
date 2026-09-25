from django.contrib import admin

from .models import EmissionLimit, Reference, Technique


class LimitInline(admin.TabularInline):
    model = EmissionLimit
    extra = 0
    fields = ("pollutant", "fuel", "capacity_min", "capacity_max", "value_min", "value_max", "unit", "section", "verified")


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ("title", "act", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "act")
    inlines = [LimitInline]


@admin.register(EmissionLimit)
class EmissionLimitAdmin(admin.ModelAdmin):
    list_display = ("pollutant", "fuel", "capacity_min", "capacity_max", "value_min", "value_max", "unit", "section", "verified", "reference")
    list_filter = ("verified", "reference", "pollutant", "medium")
    list_editable = ("verified",)
    search_fields = ("pollutant", "fuel", "installation", "section")


@admin.register(Technique)
class TechniqueAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "reference", "section")
    list_filter = ("reference",)
    search_fields = ("name", "description", "pollutants")
