from django.urls import path

from . import views

app_name = "esg_p5"
urlpatterns = [
    path("", views.index, name="index"),
]
