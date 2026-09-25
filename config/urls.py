from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "ecoservices.kz — администрирование"
admin.site.site_title = "ecoservices.kz"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
]
