from django.urls import path

from main import api_views

app_name = "api"

urlpatterns = [
    path("organizations/", api_views.organization_list, name="organization-list"),
    path("organizations/<uuid:organization_id>/", api_views.organization_detail, name="organization-detail"),
    path("organizations/<uuid:organization_id>/star/", api_views.organization_star, name="organization-star"),
]
