from django.contrib import admin

from .models import Equipment, NotifyRequest, QuoteRequest, Service, ServiceGroup


class ServiceInline(admin.TabularInline):
    model = Service
    fields = ("name", "status", "theme", "featured", "order")
    extra = 0
    show_change_link = True


@admin.register(ServiceGroup)
class ServiceGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    list_editable = ("order",)
    fields = ("name", "name_kk", "name_en", "order")
    inlines = [ServiceInline]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "group", "status", "theme", "featured", "order", "notify_count")
    list_filter = ("status", "theme", "group", "featured")
    list_editable = ("status", "featured", "order")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        (None, {"fields": ("group", "slug", "status", "theme", "tasks", "featured", "order")}),
        ("Русский", {"fields": ("name", "description")}),
        ("Қазақша", {"fields": ("name_kk", "description_kk")}),
        ("English", {"fields": ("name_en", "description_en")}),
    )

    @admin.display(description="Подписок на запуск")
    def notify_count(self, obj):
        return obj.notify_requests.count()


@admin.register(NotifyRequest)
class NotifyRequestAdmin(admin.ModelAdmin):
    list_display = ("email", "service", "created")
    list_filter = ("service",)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ("name", "theme", "order")
    list_editable = ("order",)
    fieldsets = (
        (None, {"fields": ("theme", "order")}),
        ("Русский", {"fields": ("name", "description", "parameters")}),
        ("Қазақша", {"fields": ("name_kk", "description_kk", "parameters_kk")}),
        ("English", {"fields": ("name_en", "description_en", "parameters_en")}),
    )


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ("company", "contact", "equipment", "state", "created")
    list_filter = ("state", "equipment")
    list_editable = ("state",)
    search_fields = ("company", "contact", "task")
