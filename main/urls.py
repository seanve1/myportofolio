from django.urls import path
from main.views import show_main, show_organization

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("organization/", show_organization, name="show_organization"),
]