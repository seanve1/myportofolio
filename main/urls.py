from django.urls import path
from main.views import (
    show_main,
    show_organization,
    show_education,
    create_organization,
    get_organizations_json,
    delete_organization,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("organization/", show_organization, name="show_organization"),
    path("organization/add/", create_organization, name="create_organization"),
    path('education/', show_education, name='show_education'),
    path("api/organizations/", get_organizations_json, name="get_organizations_json"),
    path("organization/<uuid:organization_id>/delete/", delete_organization, name="delete_organization"),
]