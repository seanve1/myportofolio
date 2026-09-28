from django.urls import path
from main.views import (
    show_main,

    register,
    login_user,
    logout_user,
    toggle_star,

    show_organization,
    create_organization,
    get_organizations_json,
    delete_organization,
    update_organization,

    show_education,
    create_education,
    update_education,
    delete_education,
    get_educations_json,
)

app_name = "main"

urlpatterns = [

    path(
        "",
        show_main,
        name="show_main"
    ),

    path(
        "register/",
        register,
        name="register"
    ),

    path(
        "login/",
        login_user,
        name="login"
    ),

    path(
        "logout/",
        logout_user,
        name="logout"
    ),

    # ORGANIZATION
    path(
        "organization/",
        show_organization,
        name="show_organization"
    ),

    path(
        "organization/add/",
        create_organization,
        name="create_organization"
    ),

    path(
        "organization/<uuid:organization_id>/delete/",
        delete_organization,
        name="delete_organization"
    ),

    path(
        "api/organizations/",
        get_organizations_json,
        name="get_organizations_json"
    ),

    path(
        "organization/<uuid:organization_id>/star/",
        toggle_star,
        name="toggle_star"
    ),

    # EDUCATION
    path(
        "education/",
        show_education,
        name="show_education"
    ),

    path(
        "education/add/",
        create_education,
        name="create_education"
    ),

    path(
        "organization/<uuid:organization_id>/update/",
        update_organization,
        name="update_organization"
    ),

    path(
        "education/<uuid:education_id>/update/",
        update_education,
        name="update_education"
    ),

    path(
        "education/<uuid:education_id>/delete/",
        delete_education,
        name="delete_education"
    ),

    path(
        "api/educations/",
        get_educations_json,
        name="get_educations_json"
    ),
]